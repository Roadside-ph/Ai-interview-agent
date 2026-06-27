"""
面试题检索模块
最基础的版本：按 tag 关键词匹配
后面会换成向量检索
"""

from app.data_loader import load_questions


def search_by_tag(questions: list[dict], keyword: str) -> list[dict]:
    """
    按 tag 关键词搜索题目

    参数:
        questions: 题目列表（从 load_questions 拿到的）
        keyword: 搜索关键词，比如 "装饰器"

    返回:
        包含该关键词的题目列表
    """
    results = []

    for q in questions:
        # q["tags"] 是一个列表，比如 ["Python", "装饰器", "函数"]
        # keyword 是否在这个列表里
        if keyword in q["tags"]:
            results.append(q)

    return results


def search_by_difficulty(questions: list[dict], max_difficulty: int) -> list[dict]:
    """
    按难度筛选题目

    参数:
        questions: 题目列表
        max_difficulty: 最大难度（包含）

    返回:
        难度 <= max_difficulty 的题目列表
    """
    results = []

    for q in questions:
        if q["difficulty"] <= max_difficulty:
            results.append(q)

    return results


# 如果直接运行这个文件，做个简单测试
if __name__ == "__main__":
    # 加载题目
    questions = load_questions("data/questions.json")

    # 测试按 tag 搜索
    print("=" * 40)
    print("搜索 tag='装饰器' 的题目：")
    results = search_by_tag(questions, "装饰器")
    for q in results:
        print(f"  [{q['id']}] {q['question']}")

    # 测试按难度筛选
    print("=" * 40)
    print("难度 <= 2 的题目：")
    results = search_by_difficulty(questions, 2)
    for q in results:
        print(f"  [{q['id']}] {q['question']} (难度: {q['difficulty']})")
