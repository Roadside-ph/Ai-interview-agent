import asyncio
import httpx

async def fetch_url(client: httpx.AsyncClient, url: str) -> dict:
    """用异步客户端发GET请求"""
    print(f"开始请求：{url}")
    response = await client.get(url)
    print(f"完成请求：{url}")
    return response.json()

async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:
        results = await asyncio.gather(
            fetch_url(client,"https://httpbin.org/get"),
            fetch_url(client,"https://httpbin.org/ip"),
            fetch_url(client,"https://httpbin.org/user-agent")
        )

        print(f"\n收到 {len(results)} 个响应")
        for i,result in enumerate(results):
            print(f"响应{i+1}：{list(result.keys())}")

asyncio.run(main())