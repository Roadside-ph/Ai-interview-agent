"""异步版 LLMClient：用 httpx.AsyncClient 调用 DeepSeek API"""

import httpx
from typing import Any
from app.logger import setup_logger

logger = setup_logger("llm_cli.async")

class AsyncLLMClient:
    """异步 LLM 客户端
    
    用法：
        async with AsyncLLMClient(api_key, base_url, model) as client:
            reply = await client.chat(messages)
    """

    def __init__(self, api_key: str, base_url: str, model: str, timeout: float = 60.0):
        """初始化异步客户端
        
        Args:
            api_key: DeepSeek API 密钥
            base_url: API 基础地址
            model: 模型名称
            timeout: 请求超时秒数
        """
        self.api_key = api_key
        self.model = model
        
        # 创建异步 HTTP 客户端
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            )

        logger.info(f"AsyncLLMClient 初始化完成，模型：{model}"
        )

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """发送聊天请求
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
            
        Returns:
            AI 回复文本
        """
        logger.info(f"调用LLM，消息数：{len(messages)}")

        # 发送 POST 请求到 /chat/completions
        response = await self._client.post(
            "/chat/completions",
            json={
                "model": self.model,
                "messages": messages,
            },
        )
        
        # 检查状态码，4xx/5xx 会抛出异常
        response.raise_for_status()

        
        # 解析响应，提取 AI 回复
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        
        logger.info(f"LLM调用成功，回复长度{len(reply)}字符")
        return reply
    
    async def close(self):
        """关闭客户端，释放连接"""
        await self._client.aclose()  # 修复：close → aclose

    async def __aenter__(self):
        """异步上下文管理器：进入时返回自身"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器：退出时自动关闭"""
        await self.close()
