"""API 客户端模块：封装 httpx 的 GET/POST 请求，加入超时和异常处理。"""

import httpx
from typing import Any
from app.exceptions import APITimeoutError, HttpError, NetworkError, ConfigError
from app.logger import setup_logger

logger = setup_logger("llm_cli.api")

class APIClient:
    """
    通用 API 客户端。
    
    用法示例：
        with APIClient("https://httpbin.org") as client:
            resp = client.get("/get")
            print(resp)
    """

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        """
        初始化客户端。
        
        Args:
            base_url: API 的基础地址，比如 https://api.deepseek.com/v1
            timeout: 请求超时秒数，默认 30 秒
        """
        # base_url 去掉末尾的 /，避免拼接路径时出现 //
        self.base_url = base_url.rstrip("/")
        # 创建 httpx 客户端实例，复用连接能提升性能
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        发送 GET 请求。
        
        Args:
            path: 请求路径，比如 /get、/api/v1/models
            params: URL 查询参数，比如 {"page": 1}
            
        Returns:
            响应的 JSON 数据（字典格式）
            
        Raises:
            RuntimeError: 超时、HTTP 错误、网络错误时抛出
        """
        try:
            response = self._client.get(path, params=params)
            response.raise_for_status()
            return response.json()
        
        except httpx.TimeoutException:
            logger.error(f"请求超时（{self._client.timeout}秒）：{path}")
            raise APITimeoutError(
                f"请求超时（{self._client.timeout}秒）：{path}"
            )
        
        except httpx.HTTPStatusError as e:
            logger.error(f"API 返回错误状态码 {e.response.status_code}:{path}")
            raise HttpError(
                f"API 返回错误状态码 {e.response.status_code}:{path}\n"
                f"响应内容：{e.response.text[:200]}"
            )
        
        except httpx.RequestError as e:
            logger.error( f"网络请求失败：{path}")
            raise NetworkError(
                f"网络请求失败：{path}\n"
                f"错误详情：{type(e).__name__}: {e}"
            )

    def post(
        self,
        path: str,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        发送 POST 请求。
        
        Args:
            path: 请求路径
            json_data: 要发送的 JSON 数据（字典格式）
            headers: 额外的请求头
            
        Returns:
            响应的 JSON 数据
            
        Raises:
            RuntimeError: 超时、HTTP 错误、网络错误时抛出
        """
        try:
            response = self._client.post(path, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json()
        
        except httpx.TimeoutException:
            logger.error(f"请求超时（{self._client.timeout}秒）：{path}")
            raise APITimeoutError(
                f"请求超时（{self._client.timeout}秒）：{path}"
            )
        
        except httpx.HTTPStatusError as e:
            logger.error(f"API 返回错误状态码 {e.response.status_code}:{path}")
            raise HttpError(
                f"API 返回错误状态码 {e.response.status_code}：{path}\n"
                f"响应内容：{e.response.text[:200]}"
            )
        
        except httpx.RequestError as e:
            logger.error( f"网络请求失败：{path}")
            raise NetworkError(
                f"网络请求失败：{path}\n"
                f"错误详情：{type(e).__name__}: {e}"
            )

    def close(self) -> None:
        """关闭底层 HTTP 客户端，释放连接资源。"""
        self._client.close()

    def __enter__(self):
        """支持 with 语句，进入时返回自身。"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出 with 块时自动调用 close()。"""
        self.close()


# --- 测试代码 ---
if __name__ == "__main__":
    print("=== 测试 1: GET 请求 ===")
    with APIClient("https://httpbin.org") as client:
        result = client.get("/get", params={"hello": "world"})
        print(f"返回的 args 参数：{result.get('args', {})}")

    print("\n=== 测试 2: POST 请求 ===")
    with APIClient("https://httpbin.org") as client:
        result = client.post("/post", json_data={"name": "test", "msg": "你好"})
        print(f"返回的 JSON 数据：{result.get('json', {})}")

    print("\n=== 测试 3: 超时测试 ===")
    try:
        with APIClient("https://httpbin.org", timeout=0.001) as client:
            client.get("/get")
    except RuntimeError as e:
        print(f"捕获到超时错误：{e}")

    print("\n=== 测试 4: 错误状态码测试 ===")
    try:
        with APIClient("https://httpbin.org") as client:
            client.get("/status/401")
    except RuntimeError as e:
        print(f"捕获到 HTTP 错误：{e}")

    print("\n所有测试完成！")
