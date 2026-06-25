"""AI-Interview Agent 后端服务入口。

所有 API 接口都在这个文件里注册。
启动命令：uvicorn app.main:app --reload
"""

from fastapi import FastAPI, Depends
from app.schemas.interview import QuestionCreate, QuestionResponse, QuestionDetail
from app.schemas.response import ApiResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Question
from app.logger import setup_logger
from app.routers.resume import router as resume_router
from app.routers.match import router as matching_router 
from app.routers import stream

logger = setup_logger()


app = FastAPI(
    title="AI-Interview Agent",
    description="基于 RAG 与 Agent 的智能模拟面试系统",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)
app.include_router(resume_router)
app.include_router(matching_router) 
app.include_router(stream.router)

@app.get("/")
def root():
    """根路径：返回欢迎信息。"""
    return {"message": "欢迎使用 AI-Interview Agent"}


@app.get("/health")
def health():
    """健康检查：用于监控服务是否正常运行。"""
    return {"status": "ok"}


@app.get("/questions", response_model=ApiResponse)
def list_questions(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    """查看所有面试题目列表。"""
    logger.info(f"查看题目列表")
    questions = db.query(Question).all()
    start = (page - 1) * page_size
    end = start + page_size
    paginated_data = questions[start:end]
    result = [
        {
            "id": q.id,
            "title": q.title,
            "category": q.category,
            "difficulty": q.difficulty
        }
        for q in paginated_data
    ]
    return ApiResponse(
        code=200,
        message="查询成功",
        data=result
    )


@app.get("/questions/{question_id}", response_model=ApiResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """根据 ID 查看一道面试题目。

    question_id 是路径参数，比如 GET /questions/1 中的 1
    """
    logger.info(f"查看题目：{question_id}")
    question = db.query(Question).filter(Question.id == question_id).first()
    if question:
        return ApiResponse(
            code=200,
            message="查询成功",
            data={
                "id": question.id,
                "title": question.title,
                "category": question.category,
                "difficulty": question.difficulty
            }
        )
    return ApiResponse(
        code=404,
        message=f"题目{question_id}不存在",
        data=None
    )


@app.put("/questions/{question_id}", response_model=ApiResponse)
def update_question(question_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    """根据 ID 更新一道面试题目。"""
    logger.info(f"更新题目：{question_id}")
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        db_question.title = question.title
        db_question.category = question.category
        db_question.difficulty = question.difficulty
        db.commit()
        db.refresh(db_question)
        return ApiResponse(
            code=200,
            message=f"题目{question_id}更新成功",
            data={
                "id": db_question.id,
                "title": db_question.title,
                "category": db_question.category,
                "difficulty": db_question.difficulty
            }
        )
    return ApiResponse(
        code=404,
        message=f"题目{question_id}不存在",
        data=None
    )


@app.delete("/questions/{question_id}", response_model=ApiResponse)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """根据 ID 删除一道题目。"""
    logger.warning(f"删除题目：{question_id}")
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
        return ApiResponse(
            code=200,
            message=f"题目{question_id}删除成功",
            data=None
        )
    return ApiResponse(
        code=404,
        message=f"题目{question_id}不存在",
        data=None
    )


@app.post("/questions", response_model=ApiResponse)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    """创建一道面试题目。"""
    logger.info(f"创建题目：{question.title}")
    db_question = Question(
        title=question.title,
        category=question.category,
        difficulty=question.difficulty
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return ApiResponse(
        code=200,
        message=f"创建题目成功：题目ID为{db_question.id}",
        data={
            "id": db_question.id,
            "title": db_question.title,
            "category": db_question.category,
            "difficulty": db_question.difficulty
        }
    )


@app.post("/questions/detail", response_model=QuestionDetail)
def create_question_detail(question: QuestionDetail):
    """创建带标签的题目详情。

    演示嵌套模型：QuestionDetail 里包含 Tag 列表。
    前端发来的 JSON 里，tags 是一个数组，每个元素都有 name 字段。
    """
    return question
