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

    config = load_config()
    client = DeepSeekClient(config)

    try:
        prompt = RESUME_PARSE_PROMPT.format(resume_text=req.resume_text)
        messages = [{"role": "user", "content": prompt}]
        result = await client.chat_with_schema(messages, ResumeInfo)
        return ApiResponse(
            code=200,
            message="简历解析成功",
            data=result
        )
    except Exception as e:
        return ApiResponse(
            code=500,
            message=f"简历解析失败:{str(e)}",
            data=None
        )
    finally:
        await client.aclose()
