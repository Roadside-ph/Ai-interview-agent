import pytest
import httpx
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from app.config import AppConfig
from app.llm_client import DeepSeekClient


# 创建一个测试用的配置
@pytest.fixture
def config():
    return AppConfig(
        api_key="test-key",
        base_url="https://api.deepseek.com/v1",
        model_name="deepseek-chat",
        history_dir=Path("./test_data")
    )


# 创建客户端实例
@pytest.fixture
def client(config):
    return DeepSeekClient(config)


# 辅助函数：把普通列表变成异步迭代器
async def aiter(items):
    for item in items:
        yield item


# 测试1：正常调用，能拿到回复
@pytest.mark.asyncio
async def test_chat_returns_content(client):
    """正常调用时，chat 应该返回 LLM 的回复内容"""
    # 模拟 API 返回的数据
    mock_data = {
        "choices": [
            {"message": {"content": "你好！"}}
        ]
    }

    # 用 mock 替换 _chat_once 方法
    with patch.object(client, "_chat_once", new_callable=AsyncMock) as mock:
        mock.return_value = mock_data
        result = await client.chat([{"role": "user", "content": "你好"}])

    assert result == "你好！"


# 测试2：429 错误时应该重试
@pytest.mark.asyncio
async def test_chat_retries_on_429(client):
    """遇到 429（限流）时，应该自动重试"""
    # 第一次返回 429，第二次返回成功
    error_response = httpx.Response(429)
    success_data = {"choices": [{"message": {"content": "成功"}}]}

    mock = AsyncMock()
    mock.side_effect = [
        httpx.HTTPStatusError(
            "rate limited",
            request=httpx.Request("POST", "/"),
            response=error_response
        ),
        success_data
    ]

    with patch.object(client, "_chat_once", mock):
        # patch asyncio.sleep 避免真的等待
        with patch("app.llm_client.asyncio.sleep", new_callable=AsyncMock):
            result = await client.chat([{"role": "user", "content": "测试"}])

    assert result == "成功"
    assert mock.call_count == 2  # 调用了2次（1次失败 + 1次成功）


# 测试3：401 错误不应该重试，直接报错
@pytest.mark.asyncio
async def test_chat_no_retry_on_401(client):
    """遇到 401（认证失败）时，不应该重试，直接报错"""
    error_response = httpx.Response(401)

    mock = AsyncMock()
    mock.side_effect = httpx.HTTPStatusError(
        "unauthorized",
        request=httpx.Request("POST", "/"),
        response=error_response
    )

    with patch.object(client, "_chat_once", mock):
        with pytest.raises(httpx.HTTPStatusError):
            await client.chat([{"role": "user", "content": "测试"}])

    assert mock.call_count == 1  # 只调用了1次，没有重试


# 测试4：流式输出能逐字返回
@pytest.mark.asyncio
async def test_chat_stream_yields_content(client):
    """chat_stream 应该逐字返回内容"""
    # 模拟 SSE 数据：三个字 + 结束标记
    sse_lines = [
        'data: {"choices":[{"delta":{"content":"你"}}]}',
        'data: {"choices":[{"delta":{"content":"好"}}]}',
        'data: {"choices":[{"delta":{"content":"！"}}]}',
        'data: [DONE]'
    ]

    # 模拟 stream 响应
    mock_response = AsyncMock()
    mock_response.raise_for_status = MagicMock()
    # aiter_lines() 返回一个异步迭代器
    mock_response.aiter_lines = lambda: aiter(sse_lines)

    # 模拟 stream 上下文管理器
    mock_cm = AsyncMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
    mock_cm.__aexit__ = AsyncMock(return_value=False)

    with patch.object(client._client, "stream", return_value=mock_cm):
        result = []
        async for chunk in client.chat_stream([{"role": "user", "content": "你好"}]):
            result.append(chunk)

    assert result == ["你", "好", "！"]
