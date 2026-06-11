"""对话历史持久化模块：把聊天记录保存为 JSON 文件，也能读取回来。"""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime


def save_history(
    messages: list[dict[str, str]],
    history_dir: Path,
    filename: Optional[str] = None,
) -> Path:
    """
    将对话历史保存为 JSON 文件。

    Args:
        messages: 对话消息列表，每条消息是一个包含 'role' 和 'content' 的字典
        history_dir: 历史记录保存目录
        filename: 可选的文件名，如果不提供则使用时间戳生成

    Returns:
        保存的文件路径
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.json"

    file_path = history_dir / filename

    try:
        file_path.write_text(
            json.dumps(messages, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError as e:
        raise OSError(f"保存对话历史失败：{e}") from e

    return file_path


def load_history(file_path: Path) -> list[dict[str, str]]:
    """
    从 JSON 文件加载对话历史。

    Args:
        file_path: 历史记录文件路径

    Returns:
        对话消息列表，文件不存在时返回空列表
    """
    if not file_path.exists():
        return []

    try:
        content = file_path.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"警告：历史文件格式损坏 {file_path}：{e}")
        return []
    except OSError as e:
        print(f"警告：读取历史文件失败 {file_path}：{e}")
        return []


def list_histories(history_dir: Path) -> list[Path]:
    """
    列出历史记录目录下的所有 JSON 文件，按时间倒序排列。

    Args:
        history_dir: 历史记录保存目录

    Returns:
        JSON 文件路径列表
    """
    if not history_dir.exists():
        return []

    files = list(history_dir.glob("*.json"))
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files


if __name__ == "__main__":
    from app.config import load_config

    config = load_config()

    test_messages = [
        {"role": "user", "content": "你好！"},
        {"role": "assistant", "content": "你好！有什么我可以帮助你的吗？"},
    ]

    filepath = save_history(test_messages, config.history_dir)
    print(f"历史记录已保存到：{filepath}")

    loaded_messages = load_history(filepath)
    print(f"读取回来 {len(loaded_messages)} 条消息：")
    for msg in loaded_messages:
        print(f"  [{msg['role']}] {msg['content']}")

    all_history = list_histories(config.history_dir)
    print(f"共有 {len(all_history)} 个历史文件")
