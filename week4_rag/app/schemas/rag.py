"""RAG 检索相关数据模型。

定义搜索请求、生成请求和返回数据的结构。
"""

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """语义搜索请求：用户输入查询文字，返回最相似的面试题。

    query: 用户想搜索的问题，比如 "Python 异步编程怎么学"
    top_k: 返回最相似的几道题，默认 3 道
    """

    query: str = Field(..., min_length=1, description="搜索查询文字")
    top_k: int = Field(default=3, ge=1, le=10, description="返回题目数量")


class GenerateRequest(BaseModel):
    """RAG 生成请求：用户输入问题，系统检索相关题目后让 LLM 生成答案。

    question: 用户想问的面试问题
    top_k: 检索相关题目数量，默认 3 道
    """

    question: str = Field(..., min_length=1, description="用户问题")
    top_k: int = Field(default=3, ge=1, le=10, description="检索题目数量")


class SourceItem(BaseModel):
    """检索到的一道参考题目。

    id: 题目 ID
    question: 题目文字
    answer: 参考答案
    tags: 标签（逗号分隔）
    similarity: 相似度分数，0~1，越高越相似
    """

    id: str = Field(..., description="题目 ID")
    question: str = Field(..., description="题目文字")
    answer: str = Field(..., description="参考答案")
    tags: str = Field(..., description="标签")
    similarity: float = Field(..., description="相似度分数")
