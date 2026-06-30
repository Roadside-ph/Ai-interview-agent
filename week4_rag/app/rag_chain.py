from app.vector_store import VectorStore
from app.llm_client import DeepSeekClient


class RAGChain:
    def __init__(self, vector_store: VectorStore, llm_client: DeepSeekClient):
        self._store = vector_store
        self._llm = llm_client

    def _build_prompt(self, question: str, sources: list[dict]) -> str:
        context_parts = []
        for i, src in enumerate(sources, 1):
            context_parts.append(
                f"参考题目 {i} \n"
                f"题目 {src['question']}\n"
                f"参考答案： {src['answer']}\n"
                f"标签：{src['tags']}"
            )
        context = "\n\n".join(context_parts)
        prompt = (
            f"你是一个专业的面试官助手。\n"
            f"请参考以下面试题来回答用户的问题，回答要专业、准确。\n\n"
            f"{context}\n\n"
            f"【用户问题】\n{question}"
        )
        return prompt

    async def answer(self, question: str, top_k: int = 3) -> dict:
        # 第 1 步：R = Retrieval（检索）
        sources = self._store.search(question, top_k=top_k)

        # 第 2 步：拼 Prompt
        prompt_text = self._build_prompt(question, sources)

        # 第 3 步：G = Generation（生成）
        messages = [{"role": "user", "content": prompt_text}]
        answer_text = await self._llm.chat(messages)

        # 第 4 步：打包返回
        return {
            "answer": answer_text,
            "sources": sources,
        }


# 测试：直接运行此文件
if __name__ == "__main__":
    import asyncio
    from app.config import load_config

    async def main():
        # 准备两个"零件"
        config = load_config()
        store = VectorStore()
        llm = DeepSeekClient(config)

        # 确保向量库已初始化（如果还没入库，先入库）
        store.init_collection("data/questions.json")

        # 创建 RAG 链路
        chain = RAGChain(store, llm)

        # 测试一个问题
        question = "Python 异步编程怎么做？"
        print(f"用户提问：{question}")
        print("=" * 60)

        result = await chain.answer(question)

        print(f"\nAI 回答：\n{result['answer']}\n")
        print("=" * 60)
        print("参考题目：")
        for i, src in enumerate(result["sources"], 1):
            print(f"  {i}. [{src['similarity']}] {src['question']}")

        # 清理 httpx 连接
        await llm.aclose()

    asyncio.run(main())
