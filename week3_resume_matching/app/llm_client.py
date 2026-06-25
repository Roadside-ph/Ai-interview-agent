import httpx
import asyncio
import logging
from app.config import AppConfig

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self, config: AppConfig) -> None:
        self.api_key = config.api_key
        self.model = config.model_name
        self.base_url = config.base_url
        self.max_retries = 3
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=60.0
        )

    async def _chat_once(self, messages: list[dict[str, str]]) -> dict:
        import time

        headers = {"Authorization": f"Bearer {self.api_key}"}

        json_data = {
            "model": self.model,
            "messages": messages
        }

        start_time = time.time()
        logger.info(f"开始请求，模型：{self.model}")

        response = await self._client.post(
            "/chat/completions",
            json=json_data,
            headers=headers
        )

        elapsed = time.time() - start_time
        logger.info(
            f"请求完成，状态码：{response.status_code}，"
            f"耗时：{elapsed:.2f}秒"
        )

        response.raise_for_status()
        return response.json()

    async def chat(self, messages: list[dict[str, str]]) -> str:
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                data = await self._chat_once(messages)
                return data["choices"][0]["message"]["content"]

            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                last_error = e

                if status_code in (401, 403):
                    logger.error(f"认证失败，状态码：{status_code}，不重试")
                    raise
                logger.warning(
                    f"请求失败，状态码：{status_code}，"
                    f"第{attempt}/{self.max_retries}次重试"
                )

            except httpx.TimeoutException as e:
                last_error = e
                logger.warning(
                    f"请求超时，第{attempt}/{self.max_retries}次重试"
                )

            except httpx.ConnectError as e:
                last_error = e
                logger.warning(
                    f"连接失败，第{attempt}/{self.max_retries}次重试"
                )

            if attempt < self.max_retries:
                wait_time = 2 ** (attempt - 1)
                logger.info(f"等待{wait_time}秒后重试...")
                await asyncio.sleep(wait_time)

        logger.error(f"重试{self.max_retries}次后仍然失败了")
        raise last_error

    async def chat_stream(self, messages: list[dict[str, str]]):
        import json
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                json_data = {
                    "model": self.model,
                    "messages": messages,
                    "stream": True
                }
                logger.info(f"开始流式请求，模型：{self.model}")

                async with self._client.stream(
                    "POST",
                    "/chat/completions",
                    json=json_data,
                    headers=headers
                ) as response:
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        data_str = line[6:]

                        if data_str.strip() == "[DONE]":
                            break

                        data = json.loads(data_str)
                        delta = data["choices"][0]["delta"]

                        if "content" in delta:
                            yield delta["content"]
                    
                logger.info("流式传输完成")
                return
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                last_error = e

                if status_code in (401, 403):
                    logger.error(f"认证失败，状态码：{status_code}, 不重试")
                    raise

                logger.warning(
                    f"流式请求失败，状态码：{status_code}，"
                    f"第{attempt}/{self.max_retries}次重试"
                )

            except httpx.TimeoutException as e:
                    last_error = e
                    logger.error(f"流式请求超时，第{attempt}/{self.max_retries}次重试")
            
            except httpx.ConnectError as e:
                last_error = e
                logger.error(f"流式连接失败，第{attempt}/{self.max_retries}次重试")

            if attempt < self.max_retries:
                wait_time = 2 ** (attempt - 1)
                logger.info(f"等待{wait_time}秒后重试")
                await asyncio.sleep(wait_time)

        logger.error(f"流式请求失败，第{attempt}/{self.max_retries}次重试")
        raise last_error

                    


    async def chat_with_schema(
        self,
        messages: list[dict[str, str]],
        schema_class: type
    ) -> dict:
        """调用大模型，返回校验后的 Pydantic 对象"""
        import json as json_lib

        # 第 1 步：发消息给大模型，拿到文字回复
        text = await self.chat(messages)

        # 第 2 步：清理大模型返回的文字
        text = text.strip()
        if text.startswith("```"):
            # 大模型有时会用 markdown 代码块包裹 JSON，需要去掉
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        # 第 3 步：把 JSON 字符串解析成 Python 字典
        data = json_lib.loads(text)

        # 第 4 步：用 Pydantic 模型校验，返回合格的数据对象
        return schema_class(**data)

    async def aclose(self) -> None:
        await self._client.aclose()
