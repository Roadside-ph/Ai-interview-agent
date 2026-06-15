from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "欢迎" in response.json()["message"]

def test_create_question():
    data = {
             "title": "什么是闭包？",
             "category": "Python 基础",
             "difficulty": 3
         }
    response = client.post("/questions", json=data)
    assert response.status_code == 200 
    assert response.json()["data"]["title"] == "什么是闭包？"

def test_get_question():
    create_response = client.post("/questions", json={
             "title": "什么是装饰器？",
             "category": "Python 进阶",
             "difficulty": 4
         })
    question_id = create_response.json()["data"]["id"]
    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "什么是装饰器？"

def test_delete_question():
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

    