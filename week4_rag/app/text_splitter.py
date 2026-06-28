"""
文本切分模块
负责把面试题数据切分成小块（chunk），方便后续 Embedding 和检索
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 从同目录下的 data_loader 导入加载函数
from app.data_loader import load_questions


def questions_to_documents(questions: list[dict]) -> list[Document]:
    """
    把题目字典列表转换成 LangChain Document 对象列表

    参数:
        questions: load_questions() 返回的字典列表

    返回:
        Document 对象列表，每个文档包含：
        - page_content: 题目 + 答案 + 关键点（合并成一段文字）
        - metadata: 题目ID、难度、岗位、标签（方便后续筛选）
    """
    documents = []

    for q in questions:
        # 把题目、答案、关键点拼成一段文字
        content = f"题目：{q['question']}\n"
        content += f"答案：{q['answer']}\n"
        content += f"关键点：{', '.join(q['key_points'])}"

        # metadata 存储结构化信息，方便后续按标签筛选
        metadata = {
            "id": q["id"],
            "difficulty": q["difficulty"],
            "job_role": q["job_role"],
            "tags": ", ".join(q["tags"])  # 列表转字符串，方便存储
        }

        # 创建 Document 对象
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    print(f"转换了 {len(documents)} 道题目为 Document 对象")
    return documents


def split_documents(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[Document]:
    """
    把 Document 列表切分成小块

    参数:
        documents: questions_to_documents() 返回的文档列表
        chunk_size: 每个 chunk 最大字符数（默认 500）
        chunk_overlap: 相邻 chunk 重叠字符数（默认 50）

    返回:
        切分后的 Document 列表
    """
    # 创建切分器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,  # 用字符长度计算（也可以用 token 数）
        separators=["\n\n", "\n", " ", ""]  # 分隔符优先级
    )

    # 执行切分
    chunks = splitter.split_documents(documents)

    print(f"切分完成：{len(documents)} 个文档 → {len(chunks)} 个 chunk")
    print(f"参数：chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")

    return chunks


def demo_chunk_sizes(file_path: str) -> None:
    """
    演示不同 chunk_size 的切分效果

    参数:
        file_path: questions.json 的路径
    """
    print("=" * 60)
    print("演示：不同 chunk_size 的切分效果")
    print("=" * 60)

    # 1. 加载数据
    questions = load_questions(file_path)
    if not questions:
        print("没有加载到题目数据")
        return

    # 2. 转换成 Document
    documents = questions_to_documents(questions)

    # 3. 用不同 chunk_size 切分，对比效果
    for size in [200, 500, 1000]:
        print(f"\n--- chunk_size={size} ---")
        chunks = split_documents(documents, chunk_size=size, chunk_overlap=50)

        # 打印前 3 个 chunk 的内容（截取前 100 字符）
        for i, chunk in enumerate(chunks[:3]):
            print(f"\n[chunk {i+1}] 长度={len(chunk.page_content)}")
            print(f"内容预览: {chunk.page_content[:100]}...")
            print(f"metadata: {chunk.metadata}")


if __name__ == "__main__":
    # 直接运行这个文件时，演示切分效果
    import sys
    from pathlib import Path

    # 找到 data/questions.json 的路径
    # __file__ 是当前文件的路径，往上找两级就是 week4_rag/
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "data" / "questions.json"

    if not data_path.exists():
        print(f"找不到数据文件: {data_path}")
        sys.exit(1)

    demo_chunk_sizes(str(data_path))
