from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ========== 第 1 层：接口能通 ==========

def test_root():
    """GET / 返回欢迎信息"""
    response = client.get("/")
    assert response.status_code == 200
    assert "欢迎" in response.json()["message"]


def test_health():
    """GET /health 返回 ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ========== 第 2 层：CRUD 数据逻辑 ==========

def test_create_question():
    """创建一道题目，返回的数据和传入的一致"""
    data = {
        "title": "什么是闭包？",
        "category": "Python 基础",
        "difficulty": 3
    }
    response = client.post("/questions", json=data)
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "什么是闭包？"
    assert response.json()["data"]["category"] == "Python 基础"
    assert response.json()["data"]["difficulty"] == 3


def test_get_question():
    """创建后再查询，数据一致"""
    create_response = client.post("/questions", json={
        "title": "什么是装饰器？",
        "category": "Python 进阶",
        "difficulty": 4
    })
    question_id = create_response.json()["data"]["id"]
    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "什么是装饰器？"
    assert response.json()["data"]["category"] == "Python 进阶"
    assert response.json()["data"]["difficulty"] == 4


def test_update_question():
    """创建后修改题目，再查询确认修改生效"""
    # 先创建
    create_response = client.post("/questions", json={
        "title": "什么是 GIL？",
        "category": "Python 进阶",
        "difficulty": 5
    })
    question_id = create_response.json()["data"]["id"]

    # 修改 title 和 difficulty
    update_response = client.put(f"/questions/{question_id}", json={
        "title": "GIL 是什么？如何绕过？",
        "category": "Python 进阶",
        "difficulty": 4
    })
    assert update_response.status_code == 200
    assert "更新成功" in update_response.json()["message"]

    # 再查询，确认修改生效
    get_response = client.get(f"/questions/{question_id}")
    assert get_response.json()["data"]["title"] == "GIL 是什么？如何绕过？"
    assert get_response.json()["data"]["difficulty"] == 4


def test_delete_question():
    """创建后删除，再查询返回 404"""
    create_response = client.post("/questions", json={
        "title": "什么是 GIL？",
        "category": "Python 进阶",
        "difficulty": 5
    })
    question_id = create_response.json()["data"]["id"]
    delete_response = client.delete(f"/questions/{question_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/questions/{question_id}")
    assert get_response.json()["code"] == 404


def test_list_questions():
    """创建几道题后，列表接口能返回"""
    # 先创建 2 道题
    client.post("/questions", json={
        "title": "题目A",
        "category": "测试",
        "difficulty": 1
    })
    client.post("/questions", json={
        "title": "题目B",
        "category": "测试",
        "difficulty": 2
    })

    # 查询列表
    response = client.get("/questions")
    assert response.status_code == 200
    data = response.json()["data"]
    # 列表里应该有数据（至少 2 条）
    assert len(data) >= 2


# ========== 第 3 层：边界情况 ==========

def test_get_nonexistent():
    """查询不存在的题目，返回 code=404"""
    response = client.get("/questions/99999")
    assert response.status_code == 200  # HTTP 状态码是 200
    assert response.json()["code"] == 404  # 业务 code 是 404
    assert "不存在" in response.json()["message"]


def test_delete_nonexistent():
    """删除不存在的题目，返回 code=404"""
    response = client.delete("/questions/99999")
    assert response.status_code == 200
    assert response.json()["code"] == 404


def test_difficulty_out_of_range():
    """难度超出 1-5 范围，返回 422 校验错误"""
    response = client.post("/questions", json={
        "title": "测试题目",
        "category": "测试",
        "difficulty": 10  # 超出范围
    })
    assert response.status_code == 422


def test_missing_title():
    """缺少必填字段 title，返回 422"""
    response = client.post("/questions", json={
        "category": "测试",
        "difficulty": 3
        # 没有 title
    })
    assert response.status_code == 422


def test_pagination():
    """分页测试：page=1 和 page=2 返回不同数据"""
    # 先创建 3 道题
    for i in range(3):
        client.post("/questions", json={
            "title": f"分页测试题{i}",
            "category": "测试",
            "difficulty": 1
        })

    # 每页 1 条，取第 1 页和第 2 页
    page1 = client.get("/questions?page=1&page_size=1")
    page2 = client.get("/questions?page=2&page_size=1")

    # 两页的数据应该不一样
    data1 = page1.json()["data"]
    data2 = page2.json()["data"]
    assert len(data1) == 1
    assert len(data2) == 1
    assert data1[0]["id"] != data2[0]["id"]
