"""AI-Interview Agent 后端服务入口。

所有 API 接口都在这个文件里注册。
启动命令：uvicorn app.main:app --reload
"""

# 从 fastapi 框架导入 FastAPI 类
from fastapi import FastAPI

# 从 schemas 模块导入我们定义的 Pydantic 数据模型
# QuestionCreate: 创建题目时的请求体格式
# QuestionResponse: 创建成功后的响应体格式
# QuestionDetail: 带标签的题目详情格式（嵌套模型）
from app.schemas.interview import QuestionCreate, QuestionResponse, QuestionDetail
from app.schemas.response import ApiResponse

# ========== 内存存储（临时方案） ==========
# 用 list 存储所有题目数据，每个题目是一个 dict
# 注意：服务器重启后数据会丢失，后面会换成数据库
questions_db: list[dict] = []

# 自增 ID 计数器，每创建一道题目就 +1
_next_id: int = 1


# ========== 创建 FastAPI 应用实例 ==========
# title 和 description 会显示在 Swagger 自动文档页面里
# 访问 http://127.0.0.1:8000/docs 可以看到自动生成的 API 文档
app = FastAPI(
    title="AI-Interview Agent",
    description="基于 RAG 与 Agent 的智能模拟面试系统",
    version="0.1.0",
)


# ========== 接口定义 ==========

@app.get("/")
def root():
    """根路径：返回欢迎信息。"""
    return {"message": "欢迎使用 AI-Interview Agent"}


@app.get("/health")
def health():
    """健康检查：用于监控服务是否正常运行。"""
    return {"status": "ok"}


@app.get("/questions", response_model=ApiResponse)
def list_questions(page:int=1,page_size:int = 10):
    """查看所有面试题目列表。"""
    # 直接返回整个列表，FastAPI 会自动转成 JSON
    start = (page - 1) * page_size
    end = start + page_size
    paginated_data = questions_db[start:end]
    
    return ApiResponse(
        code=200,
        message="查询成功",
        data=paginated_data,
    )


@app.get("/questions/{question_id}", response_model=ApiResponse)
def get_question(question_id: int):
    """根据 ID 查看一道面试题目。

    question_id 是路径参数，比如 GET /questions/1 中的 1
    """
    # 遍历所有题目，找到 id 匹配的那个
    for q in questions_db:
        if q["id"] == question_id:
            return ApiResponse(
                code=200,
                message="查询成功",
                data=q  
            )
    # 没找到就返回错误信息
    return ApiResponse(
        code=404,
        message=f"题目{question_id}不存在",
        data=None
    )

@app.put("/questions/{question_id}", response_model=ApiResponse)
def update_question(question_id: int, question: QuestionCreate):
    """根据 ID 更新一道面试题目。

    question_id: 路径参数，指定要更新哪道题
    question: 请求体，包含新的 title、category、difficulty
    """
    # 遍历找到目标题目
    for q in questions_db:
        if q["id"] == question_id:
            # 用新数据覆盖旧数据
            q["title"] = question.title
            q["category"] = question.category
            q["difficulty"] = question.difficulty
            return ApiResponse(
                     code=200,
                     message=f"题目{question_id}更新成功",
                     data=q
            )
    # 没找到返回错误
    return ApiResponse(
            code=404,
            message=f"题目{question_id}不存在",
            data=None
    )

@app.delete("/questions/{question_id}", response_model=ApiResponse)
def delete_question(question_id: int):
    """根据 ID 删除一道题目。

    使用 enumerate 获取下标，用 pop 删除
    """
    # enumerate 同时获取下标 i 和数据 q
    for i, q in enumerate(questions_db):
        if q["id"] == question_id:
            # pop(i) 删除并返回第 i 个元素
            questions_db.pop(i)
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

# ========== POST 接口（创建题目） ==========

# response_model=QuestionResponse 告诉 FastAPI：
# 这个接口的返回值必须符合 QuestionResponse 的结构
# 好处：
#   1. Swagger 文档会自动显示返回的 JSON 格式
#   2. 如果你 return 的 dict 里有多余字段，FastAPI 会自动过滤掉
#   3. 如果你漏了必填字段，FastAPI 会报错提醒你
@app.post("/questions", response_model=ApiResponse)
def create_question(question: QuestionCreate):
    """创建一道面试题目。

    参数 question 的类型是 QuestionCreate（我们定义的请求模型）。
    返回值会被 QuestionResponse（响应模型）过滤，只保留定义过的字段。
    """
    # 声明要修改全局变量 _next_id（不加 global 会报错）
    global _next_id

    # 把 Pydantic 对象转成 dict，方便存到 questions_db
    question_dict = question.model_dump()

    # 给新题目分配一个唯一 ID
    question_dict["id"] = _next_id

    # 把题目添加到内存存储中
    questions_db.append(question_dict)

    # 保存当前 ID，然后计数器 +1
    current_id = _next_id
    _next_id += 1

    # 返回的 dict 会被 QuestionResponse 校验
    # message、category、difficulty 都在 QuestionResponse 里定义了，所以会被保留
    return ApiResponse(
        code=200,
        message=f"创建题目成功：题目ID为{current_id}",
        data=question_dict
        )


# ========== 嵌套模型演示接口 ==========

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
