"""简历解析路由。

提供简历上传和解析的 API 接口。
用户发送简历文本 → 调用大模型解析 → 返回结构化的简历信息。
"""

# ===== 第 1 部分：导入需要的工具 =====

from fastapi import APIRouter       # APIRouter：用来创建"子路由器"，把接口分组管理
from pydantic import BaseModel      # BaseModel：用来定义请求体的数据格式
from app.schemas.resume import ResumeInfo       # ResumeInfo：简历解析结果的 Pydantic 模型（Day 16 定义的）
from app.schemas.response import ApiResponse    # ApiResponse：统一响应格式（Week 2 定义的）
from app.prompts import RESUME_PARSE_PROMPT     # RESUME_PARSE_PROMPT：简历解析的 Prompt 模板（Day 16 定义的）
from app.llm_client import DeepSeekClient       # DeepSeekClient：大模型 API 客户端（Day 15 定义的）
from app.config import load_config   # load_config：从 .env 文件加载配置的函数


# ===== 第 2 部分：创建路由器实例 =====

# APIRouter 就像一个"子窗口"
# prefix="/resume"：这个窗口下所有接口都以 /resume 开头（比如 /resume/parse）
# tags=["简历解析"]：Swagger 文档里的分类标签，方便分类查看
router = APIRouter(prefix="/resume", tags=["简历解析"])


# ===== 第 3 部分：定义请求体格式 =====

# 用户发给我们的数据格式
# 用户需要在请求体里放一个 resume_text 字段，就是简历的文本内容
class ResumeRequest(BaseModel):
    """简历解析请求体。"""
    resume_text: str    # 简历文本内容


# ===== 第 4 部分：定义接口 =====

# @router.post("/parse")：在这个路由器上注册一个 POST 接口，路径是 /parse
# 因为路由器的 prefix 是 /resume，所以完整路径是 POST /resume/parse
# response_model=ApiResponse：返回值用 ApiResponse 模型来校验和序列化
@router.post("/parse", response_model=ApiResponse)
async def parse_resume(req: ResumeRequest):
    """解析简历：接收简历文本，调用大模型提取结构化信息。

    数据流：
    用户发简历文本 → 填入 Prompt 模板 → 发给大模型 → 拿到 JSON → 用 Pydantic 校验 → 返回给用户
    """

    # 第 1 步：加载配置，创建大模型客户端
    # load_config() 从 .env 文件读取 API_KEY 等配置
    # DeepSeekClient 用这个 key 去调用 DeepSeek API
    config = load_config()
    client = DeepSeekClient(config)

    # 第 2 步：把简历文本填入 Prompt 模板
    # RESUME_PARSE_PROMPT 里有个 {resume_text} 占位符
    # .format() 会把用户发来的简历文本填进去
    # 举个例子：模板是 "请解析以下简历：{resume_text}"
    #   填完后变成 "请解析以下简历：张三，3年Python经验..."
    prompt = RESUME_PARSE_PROMPT.format(resume_text=req.resume_text)

    # 第 3 步：构造消息，调用大模型
    # messages 是一个列表，每个元素是一个 dict，包含 role 和 content
    # role="user" 表示这是用户说的话
    # chat_with_schema 会调用大模型，然后用 ResumeInfo 模型来校验返回的 JSON
    messages = [{"role": "user", "content": prompt}]
    result = await client.chat_with_schema(messages, ResumeInfo)

    # 第 4 步：关闭客户端连接
    # 用完客户端必须关闭，否则会占用网络资源
    await client.aclose()

    # 第 5 步：返回统一格式的响应
    # ApiResponse 包含 code（状态码）、message（提示信息）、data（实际数据）
    # result 是大模型返回的、经过 Pydantic 校验的简历信息 dict
    return ApiResponse(
        code=200,
        message="简历解析成功",
        data=result
    )
