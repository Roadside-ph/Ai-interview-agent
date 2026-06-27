"""面试相关的数据模型。

Pydantic 模型的作用：
  - 定义请求体（前端发来的 JSON）应该长什么样
  - 定义响应体（后端返回的 JSON）应该长什么样
  - 自动校验数据类型和约束，不合格直接返回 422 错误
"""

from pydantic import BaseModel, Field


class QuestionCreate(BaseModel):
    """创建面试题目的请求模型。

    当前端发送 POST 请求创建一道面试题时，
    请求体的 JSON 必须符合这个结构。

    举例，前端发来的 JSON 应该长这样：
    {
        "title": "什么是闭包？",
        "category": "Python 基础",
        "difficulty": 3
    }
    """

    # --- title：题目标题 ---
    # str 表示必须是字符串
    # Field(...) 里的三个点表示"必填"，不传就报错
    # min_length=1 表示不能为空字符串
    # max_length=200 表示最多 200 个字符
    # example 只影响 Swagger 文档里显示的示例值，不影响实际逻辑
    title: str = Field(..., min_length=1, max_length=200, example="什么是闭包？")

    # --- category：题目分类 ---
    # 比如 "Python 基础"、"FastAPI"、"算法" 等
    category: str = Field(..., min_length=1, max_length=50, example="Python 基础")

    # --- difficulty：难度等级 ---
    # ge = greater equal（大于等于），le = less equal（小于等于）
    # 所以 difficulty 的值必须在 1 到 5 之间
    # default=3 表示前端不传这个字段时，默认值是 3
    difficulty: int = Field(default=3, ge=1, le=5, example=3)


class QuestionResponse(BaseModel):
    """创建题目成功后的响应模型。

    告诉前端："创建成功后，你会收到这些字段。"

    注意：这个模型和 QuestionCreate 不一样！
    - QuestionCreate 有 title（题目标题）
    - QuestionResponse 有 message（确认消息）
    这是合理的：请求和响应的数据结构本来就可能不同。
    """

    # message：后端返回的确认消息
    # 比如 "收到题目：什么是闭包？"
    message: str = Field(..., example="收到题目：什么是闭包？")

    # category：回显题目分类
    category: str = Field(..., example="Python 基础")

    # difficulty：回显难度等级
    difficulty: int = Field(..., example=3)


class Tag(BaseModel):
    """题目标签。

    这是一个"小模型"，会被 QuestionDetail 引用。
    一个标签就一个字段：name（标签名）。
    """

    # 标签名，比如 "Python"、"面试高频"、"算法"
    name: str = Field(..., min_length=1, max_length=20, example="Python")


class QuestionDetail(BaseModel):
    """题目详情模型，演示嵌套模型。

    和 QuestionCreate 的区别：
    - QuestionCreate 只有 title、category、difficulty（简单字段）
    - QuestionDetail 多了 tags 和 answer（其中 tags 是嵌套模型列表）

    前端发来的 JSON 长这样：
    {
        "title": "什么是闭包？",
        "category": "Python 基础",
        "difficulty": 3,
        "tags": [
            {"name": "Python"},
            {"name": "面试高频"}
        ],
        "answer": "闭包是一个函数..."
    }

    注意 tags 的结构：它是一个列表，里面每个元素都必须符合 Tag 的结构。
    这就是"嵌套模型"——模型里套模型。
    """

    # 题目标题
    title: str = Field(..., max_length=200, example="什么是闭包？")

    # 题目分类
    category: str = Field(..., max_length=50, example="Python 基础")

    # 难度等级，1-5，默认 3
    difficulty: int = Field(default=3, ge=1, le=5, example=3)

    # --- 这是嵌套模型的关键！---
    # list[Tag] 表示这是一个列表，里面每个元素都必须是 Tag 对象
    # min_length=1 表示至少要有一个标签，不能为空列表
    # Pydantic 会自动把 JSON 里的每个 dict 转成 Tag 对象并校验
    tags: list[Tag] = Field(
        ...,
        min_length=1,
        example=[{"name": "Python"}, {"name": "面试高频"}],
    )

    # 参考答案，默认空字符串（可以不传）
    answer: str = Field(default="", max_length=2000, example="闭包是一个函数...")
