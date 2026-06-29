"""
Embedding 向量化模块
使用本地 sentence-transformers 模型把文本变成向量（不依赖外部 API）
"""

from sentence_transformers import SentenceTransformer


class Embedder:
    """
    文本 → 向量的转换器

    内部使用 sentence-transformers 本地模型：
    - 第一次运行会自动下载模型文件（约 80MB，只需一次）
    - 之后直接从本地加载，毫秒级响应
    - 不需要联网，不花钱
    """

    # 模型名：多语言迷你模型，中文英文都支持
    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self) -> None:
        """
        初始化 Embedder，加载本地模型

        注意：第一次运行会从 HuggingFace 下载模型文件，
        如果下载慢，可以设置镜像：export HF_ENDPOINT=https://hf-mirror.com
        """
        print(f"正在加载模型 {self.MODEL_NAME} ...")
        # 加载预训练模型到内存
        self._model = SentenceTransformer(self.MODEL_NAME)
        print(f"模型加载完成！")

    def embed(self, text: str) -> list[float]:
        """
        把一段文字转成向量

        参数:
            text: 要向量化的文字，比如 "Python 异步编程"

        返回:
            向量列表，每个数字是 float 类型
        """
        # encode() 返回 numpy array，用 tolist() 转成 Python 列表
        vector = self._model.encode(text)
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        批量把多段文字转成向量（一次编码一批，比逐条快）

        参数:
            texts: 要向量化的文字列表，如 ["题1", "题2", "题3"]

        返回:
            向量列表的列表，顺序与输入一致
        """
        # encode() 原生支持列表输入，返回二维数组
        vectors = self._model.encode(texts)
        return vectors.tolist()


# 测试：直接运行此文件时，验证 Embedding 功能
if __name__ == "__main__":
    # 创建 Embedder（第一次会下载模型）
    embedder = Embedder()

    # 测试 1：单个文本
    print("=" * 50)
    print("测试 1：单段文字向量化")
    text = "Python 异步编程"
    vector = embedder.embed(text)
    print(f"输入: {text}")
    print(f"向量长度: {len(vector)} 个数字")
    print(f"向量前 5 位: {vector[:5]}")

    # 测试 2：批量文本
    print("=" * 50)
    print("测试 2：批量向量化")
    texts = [
        "Python 异步编程",
        "番茄炒蛋的做法",
        "Docker 容器化部署",
    ]
    vectors = embedder.embed_batch(texts)
    for t, v in zip(texts, vectors):
        print(f"  {t}: 向量长度 {len(v)}")

    # 测试 3：验证"语义相近的文本，向量也相近"
    print("=" * 50)
    print("测试 3：语义相似度验证")
    from sentence_transformers import util

    vec_async = embedder.embed("Python 异步编程")
    vec_thread = embedder.embed("Python 多线程并发")
    vec_tomato = embedder.embed("番茄炒蛋的做法")

    # cosine_sim 计算余弦相似度：越接近 1 越相似
    sim_async_thread = util.cos_sim(vec_async, vec_thread).item()
    sim_async_tomato = util.cos_sim(vec_async, vec_tomato).item()

    print(f'"Python 异步编程" vs "Python 多线程并发": {sim_async_thread:.4f}')
    print(f'"Python 异步编程" vs "番茄炒蛋的做法": {sim_async_tomato:.4f}')
    print()
    if sim_async_thread > sim_async_tomato:
        print("✅ 符合预期：语义相近的文本，相似度更高！")
    else:
        print("❌ 不符合预期，可能需要换模型")

    print("=" * 50)
    print("测试完成！")
