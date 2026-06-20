"""统一响应格式模型。

所有 API 接口都用这个格式返回数据，前端只需要检查 code 就能判断成功/失败。
"""

from pydantic import BaseModel, Field
from typing import Any


class ApiResponse(BaseModel):
    """统一响应格式。

    code: 状态码，200=成功，其他=失败
    message: 提示信息
    data: 实际数据（可以是任意类型）
    """

    # 状态码：200 表示成功，404 表示不存在，500 表示服务器错误
    # default=200 表示不传这个字段时，默认值是 200
    code: int = Field(default=200, example=200)

    # 提示信息：成功时显示 "success"，失败时显示具体错误原因
    message: str = Field(default="success", example="success")

    # 实际数据：可以是任意类型（dict、list、None 等）
    # Any 表示不限制类型，允许返回任何数据
    data: Any = Field(default=None, example={"id": 1, "title": "什么是闭包？"})
