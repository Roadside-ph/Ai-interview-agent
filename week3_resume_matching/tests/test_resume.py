"""简历解析接口测试。

测试 /resume/parse 接口：
- 第 1 层：接口能通（HTTP 状态码正确）
- 第 2 层：数据逻辑对（模拟大模型返回，检查响应格式）
- 第 3 层：边界情况（空文本、模拟 API 报错）
"""

from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 模拟大模型返回的固定数据
MOCK_RESUME_RESULT = {
    "name": "张三",
    "education": ["北京大学", "计算机科学与技术"],
    "skills": ["Python", "FastAPI", "SQLAlchemy"],
    "experience_years": 3,
    "project_summary": ["AI 面试系统", "电商后端"]
}


# ========== 第 1 层：接口能通 ==========

@patch("app.routers.resume.DeepSeekClient")
def test_parse_resume_success(MockClient):
    """POST /resume/parse 接口能通，返回 200"""
    # 设置 mock：让 chat_with_schema 返回固定数据
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(return_value=MOCK_RESUME_RESULT)
    mock_instance.aclose = AsyncMock()

    # 发送请求
    response = client.post("/resume/parse", json={
        "resume_text": "张三，北京大学，3年Python经验"
    })

    # 检查结果
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert "成功" in response.json()["message"]


# ========== 第 2 层：数据逻辑对 ==========

@patch("app.routers.resume.DeepSeekClient")
def test_parse_resume_data(MockClient):
    """模拟大模型返回固定数据，检查响应格式正确"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(return_value=MOCK_RESUME_RESULT)
    mock_instance.aclose = AsyncMock()

    response = client.post("/resume/parse", json={
        "resume_text": "张三，北京大学，3年Python经验"
    })

    data = response.json()["data"]
    assert data["name"] == "张三"
    assert "Python" in data["skills"]
    assert data["experience_years"] == 3


# ========== 第 3 层：边界情况 ==========

@patch("app.routers.resume.DeepSeekClient")
def test_parse_resume_empty_text(MockClient):
    """空简历文本，应该也能调用（大模型处理）"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(return_value=MOCK_RESUME_RESULT)
    mock_instance.aclose = AsyncMock()

    response = client.post("/resume/parse", json={
        "resume_text": ""
    })

    # 接口应该能正常返回
    assert response.status_code == 200


@patch("app.routers.resume.DeepSeekClient")
def test_parse_resume_api_error(MockClient):
    """模拟大模型 API 报错，检查错误处理"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(side_effect=Exception("API 超时"))
    mock_instance.aclose = AsyncMock()

    response = client.post("/resume/parse", json={
        "resume_text": "测试简历"
    })

    # 应该返回 500 错误
    assert response.status_code == 200
    assert response.json()["code"] == 500
    assert "失败" in response.json()["message"]

def test_parse_resume_missing_field():
    """缺少必填字段 resume_text，返回 422"""
    response = client.post("/resume/parse", json={})
    assert response.status_code == 422
