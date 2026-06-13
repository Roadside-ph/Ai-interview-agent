"""AI-Interview Agent 后端服务入口。

所有 API 接口都在这个文件里注册。
启动命令：uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from app.schemas.interview import QuestionCreate, QuestionResponse, QuestionDetail

questions_db: list[dict] = []
_next_id: int = 1

# 创建 FastAPI 应用实例
# title 和 description 会显示在 Swagger 自动文档页面里
app = FastAPI(
    title="AI-Interview Agent",
    description="基于 RAG 与 Agent 的智能模拟面试系统",
    version="0.1.0",
)



@app.get("/")
def root():
    """根路径：返回欢迎信息。"""
    return {"message": "欢迎使用 AI-Interview Agent"}


@app.get("/health")
def health():
    """健康检查：用于监控服务是否正常运行。"""
    return {"status": "ok"}

@app.get("/questions")
def list_questions():
    """查看所有面试题目列表。"""
    return questions_db

@app.get("/questions/{question_id}")
def get_question(question_id:int):
    for q in questions_db:
        if q["id"] == question_id:
            return q
    return {"error":f"题目{question_id}不存在"}

@app.put("/questions/{question_id}")
def update_question(question_id:int, question:QuestionCreate):
    for q in questions_db:
        if q["id"] == question_id:
            q["title"] = question.title
            q["category"] = question.category
            q["difficulty"] = question.difficulty   
            return {"message":f"题目{question_id}更新成功"}
    return {"error":f"题目{question_id}不存在"}

@app.delete("/questions/{question_id}")
def delete_question(question_id: int):
    """根据 ID 删除一道题目。"""
    for i, q in enumerate(questions_db):
        if q["id"] == question_id:
            questions_db.pop(i)
            return {"message":f"题目{question_id}删除成功"}
    return {"error":f"题目{question_id}不存在"}

# response_model=QuestionResponse 告诉 FastAPI：
# 这个接口的返回值必须符合 QuestionResponse 的结构
# 好处：
#   1. Swagger 文档会自动显示返回的 JSON 格式
#   2. 如果你 return 的 dict 里有多余字段，FastAPI 会自动过滤掉
#   3. 如果你漏了必填字段，FastAPI 会报错提醒你
@app.post("/questions", response_model=QuestionResponse)
def create_question(question: QuestionCreate):
    """创建一道面试题目。

    参数 question 的类型是 QuestionCreate（我们定义的请求模型）。
    返回值会被 QuestionResponse（响应模型）过滤，只保留定义过的字段。
    """
    # 返回的 dict 会被 QuestionResponse 校验
    # message、category、difficulty 都在 QuestionResponse 里定义了，所以会被保留
    global _next_id
    question_dict = question.model_dump ()
    question_dict["id"] = _next_id

    questions_db.append(question_dict)

    current_id = _next_id
    _next_id += 1


    return {
        "message": f"创建题目成功：题目ID为{current_id}",
        "category": question.category,
        "difficulty": question.difficulty,
    }


# --- 嵌套模型演示接口 ---
# 这个接口用 QuestionDetail 作为请求模型和响应模型
# QuestionDetail 里面有 tags: list[Tag]，这就是"模型里套模型"
@app.post("/questions/detail", response_model=QuestionDetail)
def create_question_detail(question: QuestionDetail):
    """创建带标签的题目详情。

    演示嵌套模型：QuestionDetail 里包含 Tag 列表。
    前端发来的 JSON 里，tags 是一个数组，每个元素都有 name 字段。
    """
    # 直接把收到的 question 对象原样返回
    # FastAPI 会自动把 Pydantic 对象转成 dict，再转成 JSON
    # response_model=QuestionDetail 会确保返回格式正确
    return question
