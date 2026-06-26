"""岗位匹配接口测试。

测试 /matching/parse-jd 和 /matching/match 接口：
- 第 1 层：接口能通（HTTP 状态码正确）
- 第 2 层：数据逻辑对（模拟大模型返回，检查响应格式）
- 第 3 层：边界情况（空文本、模拟 API 报错）
"""

from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 模拟大模型返回的固定数据
MOCK_JD_RESULT = {
    "job_title": "Python 后端开发",
    "required_skills": ["Python", "FastAPI", "SQLAlchemy"],
    "preferred_skills": ["Docker", "Redis"],
    "experience_years": 3,
    "education_requirement": "本科"
}

MOCK_MATCH_RESULT = {
    "match_score": 85,
    "strengths": ["Python 经验丰富", "有 FastAPI 项目经验"],
    "weaknesses": ["缺少 Docker 经验"],
    "interview_topics": ["Python 基础", "FastAPI 框架", "数据库设计"]
}


# ========== 第 1 层：接口能通 ==========

@patch("app.routers.match.DeepSeekClient")
def test_parse_jd_success(MockClient):
    """POST /matching/parse-jd 接口能通，返回 200"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(return_value=MOCK_JD_RESULT)
    mock_instance.aclose = AsyncMock()

    response = client.post("/matching/parse-jd", json={
        "jd_text": "Python 后端开发，3年经验，熟悉 FastAPI"
    })

    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert "成功" in response.json()["message"]


@patch("app.routers.match.DeepSeekClient")
def test_match_success(MockClient):
    """POST /matching/match 接口能通，返回 200"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(return_value=MOCK_MATCH_RESULT)
    mock_instance.aclose = AsyncMock()

    response = client.post("/matching/match", json={
        "resume_info": "张三，3年Python经验",
        "jd_info": "Python 后端开发，3年经验"
    })

    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert "成功" in response.json()["message"]


# ========== 第 2 层：数据逻辑对 ==========

@patch("app.routers.match.DeepSeekClient")
def test_parse_jd_data(MockClient):
    """模拟大模型返回固定数据，检查响应格式正确"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(return_value=MOCK_JD_RESULT)
    mock_instance.aclose = AsyncMock()

    response = client.post("/matching/parse-jd", json={
        "jd_text": "Python 后端开发，3年经验，熟悉 FastAPI"
    })

    data = response.json()["data"]
    assert data["job_title"] == "Python 后端开发"
    assert "Python" in data["required_skills"]
    assert data["experience_years"] == 3


@patch("app.routers.match.DeepSeekClient")
def test_match_data(MockClient):
    """模拟大模型返回固定数据，检查响应格式正确"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(return_value=MOCK_MATCH_RESULT)
    mock_instance.aclose = AsyncMock()

    response = client.post("/matching/match", json={
        "resume_info": "张三，3年Python经验",
        "jd_info": "Python 后端开发，3年经验"
    })

    data = response.json()["data"]
    assert data["match_score"] == 85
    assert len(data["strengths"]) > 0
    assert len(data["weaknesses"]) > 0


# ========== 第 3 层：边界情况 ==========

@patch("app.routers.match.DeepSeekClient")
def test_parse_jd_api_error(MockClient):
    """模拟大模型 API 报错，检查错误处理"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(side_effect=Exception("API 超时"))
    mock_instance.aclose = AsyncMock()

    response = client.post("/matching/parse-jd", json={
        "jd_text": "测试 JD"
    })

    # 应该返回业务错误码 500
    assert response.status_code == 200
    assert response.json()["code"] == 500
    assert "失败" in response.json()["message"]


@patch("app.routers.match.DeepSeekClient")
def test_match_api_error(MockClient):
    """模拟大模型 API 报错，检查错误处理"""
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(side_effect=Exception("API 超时"))
    mock_instance.aclose = AsyncMock()

    response = client.post("/matching/match", json={
        "resume_info": "测试简历",
        "jd_info": "测试 JD"
    })

    # 应该返回业务错误码 500
    assert response.status_code == 200
    assert response.json()["code"] == 500
    assert "失败" in response.json()["message"]


def test_parse_jd_missing_field():
    """缺少必填字段 jd_text，返回 422"""
    response = client.post("/matching/parse-jd", json={})
    assert response.status_code == 422


def test_match_missing_field():
    """缺少必填字段，返回 422"""
    response = client.post("/matching/match", json={
        "resume_info": "测试简历"
        # 缺少 jd_info
    })
    assert response.status_code == 422
