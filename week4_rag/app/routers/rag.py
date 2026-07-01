"""RAG 检索 API 路由。

提供两个接口：
- POST /search：纯语义检索，返回相似题目
- POST /generate：RAG 完整链路，检索 + LLM 生成答案
"""

from fastapi import APIRouter
from app.schemas.rag import SearchRequest, GenerateRequest, SourceItem
from app.schemas.response import ApiResponse
from app.vector_store import VectorStore
from app.rag_chain import RAGChain
from app.llm_client import DeepSeekClient
from app.config import load_config
from app.logger import setup_logger

logger = setup_logger("rag_router")

# 创建路由，prefix="/rag" 表示所有接口路径都以 /rag 开头
# tags=["RAG 检索"] 让 Swagger UI 里分组显示
router = APIRouter(prefix="/rag", tags=["RAG 检索"])

# 在模块加载时初始化 VectorStore 和 RAGChain（只做一次）
# 这就是"单例"模式：整个服务共用同一套向量库和大模型客户端
config = load_config()
_store = VectorStore()
# 确保向量库数据已入库（如果还没入库就入库）
_store.init_collection("data/questions.json")
_llm = DeepSeekClient(config)
_chain = RAGChain(_store, _llm)


@router.post("/search", response_model=ApiResponse)
async def search(request: SearchRequest):
    """语义搜索：根据用户输入找到最相似的面试题。

    不调大模型，只做向量检索。
    比如输入 "Python 异步编程"，返回最相关的 3 道题。
    """
    logger.info(f"RAG 搜索: query='{request.query}', top_k={request.top_k}")

    # 调用向量存储的 search 方法
    sources = _store.search(request.query, top_k=request.top_k)

    # 把返回的 dict 列表转成 SourceItem 列表
    items = [SourceItem(**s) for s in sources]

    return ApiResponse(
        code=200,
        message=f"搜索完成，找到 {len(items)} 道相关题目",
        data=[item.model_dump() for item in items],
    )


@router.post("/generate", response_model=ApiResponse)
async def generate(request: GenerateRequest):
    """RAG 生成答案：检索相关题目 + 让 LLM 生成参考答案。

    完整 RAG 流程：
    1. 向量检索 → 找最相似的题目
    2. 拼 Prompt → 把参考题目和用户问题组合
    3. LLM 生成 → DeepSeek 生成参考答案
    """
    logger.info(f"RAG 生成: question='{request.question}', top_k={request.top_k}")

    # 调用 RAGChain 的 answer 方法，一步完成检索+生成
    result = await _chain.answer(request.question, top_k=request.top_k)

    # result 格式: {"answer": "生成的答案", "sources": [{题目信息}, ...]}
    sources = [SourceItem(**s) for s in result["sources"]]

    return ApiResponse(
        code=200,
        message="生成完成",
        data={
            "question": request.question,
            "answer": result["answer"],
            "sources": [s.model_dump() for s in sources],
        },
    )
