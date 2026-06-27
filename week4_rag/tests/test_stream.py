import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_stream_chat():
    """测试流式聊天接口"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        async with client.stream(
            "POST",
            "/chat/stream",
            json={"message": "你好，请用一句话介绍Python"}
        ) as response:
            assert response.status_code == 200
            
            chunks = []
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    content = line[6:]
                    if content.strip() == "[DONE]":
                        break
                    chunks.append(content)
            
            # 至少应该收到一些数据块
            assert len(chunks) > 0
            # 拼接起来应该是一段完整的文字
            full_text = "".join(chunks)
            assert len(full_text) > 0
            print(f"\n收到 {len(chunks)} 个数据块")
            print(f"完整回复：{full_text[:100]}...")
