import httpx
# response = httpx.get("https://httpbin.org/get")
# print(f"状态码：{response.status_code}")
# data = response.json()
# print(f"返回数据：{data}")

# response = httpx.post("http://httpbin.org/post",json={"name":"wangpenghui","msg":"你好"})
# print(f"状态码：{response.status_code}")
# data = response.json()
# print(f"服务器收到的JSON：{data['json']}")

print("===test1:timeout===")
try:
    response = httpx.get("https://httpbin.org/get",timeout=0.001)
    print(f"状态码：{response.status_code}")
except httpx.TimeoutException as e:
    print(f"超时，错误类型：{type(e).__name__}")
    print(f"错误信息：{e}")

print("===test2:404 Error===")
try:
    response = httpx.get("https://httpbin.org/status/404")
    print(f"状态码：{response.status_code}")
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    print(f"http错误！状态码：{e.response.status_code}")
    print(f"错误信息：{e}")

print("===test3:internet wrong===")
try:
    response = httpx.get("https://notexist12345.com",timeout=5.0)
except httpx.RequestError as e:
    print(f"网络错误！错误类型：{type(e).__name__}")
    print(f"错误信息:{e}")