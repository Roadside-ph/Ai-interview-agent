"""测试异步 LLMClient：并发调用 DeepSeek API"""

import asyncio
from app.config import load_config
from app.async_llm_client import AsyncLLMClient
from app.timer import timer


@timer
async def ask_question(client: AsyncLLMClient, question: str, index: int) -> str:
    """问一个问题并返回回答"""
    print(f"问题 {index} 开始：{question}")
    
    messages = [{"role": "user", "content": question}]
    reply = await client.chat(messages)
    
    print(f"问题 {index} 完成")
    return reply


@timer
async def main():
    """并发问 3 个问题"""
    config = load_config()
    
    # 用 async with 自动关闭客户端
    async with AsyncLLMClient(
        api_key=config.api_key,
        base_url=config.base_url,
        model=config.model_name,
    ) as client:
        
        print("=== 并发问 3 个问题 ===")
        
        # 并发执行 3 个问题
        results = await asyncio.gather(
            ask_question(client, "用一句话介绍 Python", 1),
            ask_question(client, "用一句话介绍 JavaScript", 2),
            ask_question(client, "用一句话介绍 Go 语言", 3),
        )
        
        print("\n=== 回答 ===")
        for i, reply in enumerate(results, 1):
            print(f"问题 {i}：{reply[:50]}...")  # 只显示前 50 个字


asyncio.run(main())
