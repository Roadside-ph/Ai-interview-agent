"""
面试题数据加载模块
负责从 questions.json 读取题目数据
"""

import json
from pathlib import Path


def load_questions(file_path: str) -> list[dict]:
    """
    从 JSON 文件加载面试题数据

    参数:
        file_path: JSON 文件的路径

    返回:
        题目列表，每个题目是一个字典
        如果文件不存在或解析失败，返回空列表
    """
    # 把字符串路径转成 Path 对象，方便后续操作
    path = Path(file_path)

    # 检查文件是否存在
    if not path.exists():
        print(f"文件不存在: {file_path}")
        return []

    # 读取并解析 JSON
    try:
        # encoding="utf-8" 防止 Windows 上中文乱码
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 确认读出来的是列表
        if not isinstance(data, list):
            print(f"文件格式错误: 期望列表，实际是 {type(data).__name__}")
            return []

        print(f"成功加载 {len(data)} 道题目")
        return data

    except json.JSONDecodeError as e:
        # JSON 格式写错了（比如少了逗号、多了逗号）
        print(f"JSON 解析失败: {e}")
        return []
