"""测试配置管理模块。"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch
from app.config import load_config
from app.exceptions import ConfigError


def test_load_config_success(tmp_path):
    """正常 .env 文件应该成功加载配置"""
    # 创建一个临时 .env 文件
    env_file = tmp_path / ".env"
    env_file.write_text(
        "API_KEY=test-key-123\n"
        "BASE_URL=https://api.test.com/v1\n"
        "MODEL_NAME=test-model\n"
        f"HISTORY_DIR={tmp_path / 'data'}\n"
    )

    config = load_config(env_path=str(env_file))
    assert config.api_key == "test-key-123"
    assert config.base_url == "https://api.test.com/v1"
    assert config.model_name == "test-model"


def test_load_config_missing_env_file():
    """缺少 .env 文件应该抛出 ConfigError"""
    with pytest.raises(ConfigError, match="找不到 .env 文件"):
        load_config(env_path="/不存在的路径/.env")


def test_load_config_missing_api_key(tmp_path):
    """缺少 API_KEY 应该抛出 ConfigError"""
    env_file = tmp_path / ".env"
    env_file.write_text("BASE_URL=https://api.test.com/v1\n")

    # mock 掉环境变量，确保 API_KEY 不存在
    with patch.dict(os.environ, {"API_KEY": ""}, clear=False):
        with pytest.raises(ConfigError, match="缺少 API_KEY"):
            load_config(env_path=str(env_file))
