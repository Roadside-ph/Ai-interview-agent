"""
向量存储模块
用 Chroma 存储面试题的向量，支持语义检索
"""

import chromadb
from app.embedder import Embedder
from app.data_loader import load_questions


class VectorStore:
    """
    面试题向量存储

    工作流程：
    1. 初始化时加载 Embedder 模型
    2. init_collection() 把 20 道题向量化存入 Chroma
    3. search() 接收查询文字，返回最相似的题目
    """

    def __init__(self) -> None:
        """初始化向量存储"""
        # 创建 Chroma 客户端（数据存在本地 ./chroma_data 目录）
        self._client = chromadb.PersistentClient(path="./chroma_data")

        # 创建 Embedder（加载本地模型）
        self._embedder = Embedder()

        # 集合名：相当于数据库里的"表"
        self._collection_name = "interview_questions"

    def init_collection(self, questions_path: str) -> None:
        """
        初始化集合：读取面试题，向量化，存入 Chroma

        参数:
            questions_path: questions.json 的文件路径

        注意：
        - 如果集合已存在，先删除重建（确保数据是最新的）
        - 向量化的是 question 字段（题目文字）
        - 其他字段（answer、tags 等）存在 metadata 里
        """
        # 加载面试题数据
        questions = load_questions(questions_path)
        if not questions:
            print("没有加载到题目，跳过初始化")
            return

        # 如果集合已存在，先删除（避免重复插入）
        try:
            self._client.delete_collection(self._collection_name)
            print(f"已删除旧集合 '{self._collection_name}'")
        except Exception:
            pass  # 集合不存在，不用管

        # 创建新集合，指定用余弦距离（语义相似度标准做法）
        collection = self._client.create_collection(
            name=self._collection_name,
            metadata={
                "description": "AI 面试题库，支持语义检索",
                "hnsw:space": "cosine",  # 余弦距离：0=完全相同, 2=完全相反
            },
        )

        # 准备数据：提取文本、向量化、打包 metadata
        ids = []          # 每条记录的唯一 ID
        embeddings = []   # 向量列表
        metadatas = []    # 元数据（原题信息）
        documents = []    # 原始文本（存 question 字段，方便查看）

        print(f"正在向量化 {len(questions)} 道题 ...")

        # 第一步：提取所有题目文字
        texts = [q["question"] for q in questions]

        # 第二步：批量向量化（一次调用处理全部，比逐条快）
        vectors = self._embedder.embed_batch(texts)

        # 第三步：打包数据
        for q, vec in zip(questions, vectors):
            qid = str(q["id"])  # Chroma 要求 ID 是字符串
            ids.append(qid)
            embeddings.append(vec)
            documents.append(q["question"])
            metadatas.append({
                "question": q["question"],
                "answer": q["answer"],
                "tags": ", ".join(q["tags"]),      # 列表转字符串
                "job_role": q["job_role"],
                "difficulty": q["difficulty"],      # int 会被转成 float，没关系
            })

        # 第四步：批量插入
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents,
        )

        print(f"✅ 成功存入 {len(ids)} 道题到 Chroma 集合 '{self._collection_name}'")

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        语义检索：根据查询文字，找到最相似的题目

        参数:
            query: 查询文字，比如 "Python 异步编程"
            top_k: 返回前几名（默认 3）

        返回:
            最相似的题目列表，每个元素包含:
            - id: 题目 ID
            - question: 题目文字
            - answer: 答案
            - tags: 标签
            - similarity: 相似度分数（0~1，越高越像）
        """
        # 获取集合
        collection = self._client.get_collection(self._collection_name)

        # 把查询文字向量化
        query_vector = self._embedder.embed(query)

        # 在 Chroma 中检索最相似的 top_k 条
        results = collection.query(
            query_embeddings=[query_vector],  # 注意：传的是列表
            n_results=top_k,
            include=["metadatas", "documents", "distances"],
        )

        # 整理返回结果
        items = []
        # results 是嵌套结构，因为 query_embeddings 是列表
        ids_list = results["ids"][0]           # 第一组查询的结果
        metadatas_list = results["metadatas"][0]
        distances_list = results["distances"][0]

        for i in range(len(ids_list)):
            qid = ids_list[i]
            meta = metadatas_list[i]
            distance = distances_list[i]

            # Chroma 余弦距离：0=完全相同, 2=完全相反
            # 转成相似度：1=完全相同, 0=完全无关
            similarity = 1.0 - (distance / 2.0)

            items.append({
                "id": qid,
                "question": meta["question"],
                "answer": meta["answer"],
                "tags": meta["tags"],
                "similarity": round(similarity, 4),
            })

        return items


# 测试：直接运行此文件
if __name__ == "__main__":
    print("=" * 60)
    print("初始化向量存储 ...")
    store = VectorStore()

    # 入库
    store.init_collection("data/questions.json")

    # 测试检索
    print("\n" + "=" * 60)
    print("测试检索：查找与 'Python 异步编程' 最相似的题目")
    results = store.search("Python 异步编程", top_k=3)

    for i, r in enumerate(results, 1):
        print(f"\n第 {i} 名:")
        print(f"  ID: {r['id']}")
        print(f"  题目: {r['question']}")
        print(f"  标签: {r['tags']}")
        print(f"  相似度: {r['similarity']}")

    print("\n" + "=" * 60)
    print("测试完成！")
