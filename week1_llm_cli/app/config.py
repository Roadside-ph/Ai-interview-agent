"""配置管理模块：从 .env 文件读取项目配置。"""

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv
from app.exceptions import ConfigError
from app.logger import setup_logger

logger = setup_logger("llm_cli.config")

@dataclass
class AppConfig:
    """应用配置数据类，用类型注解明确每个字段的类型。"""

    api_key: str
    base_url: str
    model_name: str
    history_dir: Path


def load_config(env_path: str = ".env") -> AppConfig:
    """
    从 .env 文件加载配置。

    Args:
        env_path: .env 文件路径，默认为项目根目录下的 .env

    Returns:
        AppConfig 实例

    Raises:
        FileNotFoundError: .env 文件不存在时抛出
        ValueError: 缺少必要的环境变量时抛出
    """
    # Path(__file__).parent.parent 指向项目根目录（week1_llm_cli/）
    project_root = Path(__file__).parent.parent
    env_file = project_root / env_path

    if not env_file.exists():
        logger.error(f"找不到 .env 文件：{env_file}")
        raise ConfigError(
            f"找不到 .env 文件：{env_file}\n"
            f"请复制 .env.example 为 .env 并填入你的 API Key"
        )

    # load_dotenv 会把 .env 里的键值对加载到 os.environ
    load_dotenv(env_file)

    # 读取配置，如果缺少则报清晰错误
    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error(f"缺少 API_KEY，请在 .env 文件中设置")
        raise ConfigError("缺少 API_KEY，请在 .env 文件中设置")

    base_url = os.getenv("BASE_URL", "https://api.openai.com/v1")
    model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    history_dir = Path(os.getenv("HISTORY_DIR", "./data"))

    # 确保 history_dir 目录存在
    history_dir.mkdir(parents=True, exist_ok=True)

    return AppConfig(
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
        history_dir=history_dir,
    )


# 测试：直接运行此文件时打印配置
if __name__ == "__main__":
    config = load_config()
    # 不打印 API Key，避免泄露
    print(f"Base URL: {config.base_url}")
    print(f"Model: {config.model_name}")
    print(f"History Dir: {config.history_dir}")
    print("配置加载成功！")
