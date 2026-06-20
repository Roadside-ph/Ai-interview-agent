# Week 2 复盘 —— FastAPI 后端骨架

> 这份文档帮你回顾 week2_fastapi 里每个文件是干什么的、它们之间怎么配合。
> 面试时用这个顺序讲：先搭架子 → 定义数据格式 → 实现功能 → 统一规范 → 接数据库 → 工程化

---

## 项目结构总览

```
week2_fastapi/
├── app/
│   ├── __init__.py              # 空文件，标记 app 是 Python 包
│   ├── main.py                  # 【入口】所有 API 接口在这里定义
│   ├── database.py              # 【数据库】SQLAlchemy 引擎 + 会话配置
│   ├── models.py                # 【表结构】数据库表模型（Question）
│   ├── logger.py                # 【日志】控制台 + 文件双输出
│   └── schemas/
│       ├── __init__.py          # 空文件，标记 schemas 是 Python 包
│       ├── interview.py         # 【数据校验】请求/响应的 Pydantic 模型
│       └── response.py          # 【统一响应】ApiResponse 包装格式
├── tests/
│   └── test_questions.py        # 【测试】4 个 pytest 测试用例
├── requirements.txt             # 依赖列表
├── .env                         # 环境变量（数据库路径等）
└── .gitignore                   # Git 忽略规则
```

---

## 文件详解

### 1. main.py —— API 接口入口

**作用**：所有 HTTP 接口都在这里定义，是整个后端的"大脑"。

**它依赖了谁**：
- `schemas/interview.py` → 用来校验请求数据
- `schemas/response.py` → 用来包装返回数据
- `database.py` → 用来获取数据库会话
- `models.py` → 用来操作数据库表
- `logger.py` → 用来记录日志

**包含 7 个接口**：

| 方法 | 路径 | 功能 | 学于 |
|------|------|------|------|
| GET | / | 返回欢迎信息 | Day 8 |
| GET | /health | 健康检查 | Day 8 |
| GET | /questions | 查看所有题目（带分页） | Day 10, 11 |
| GET | /questions/{id} | 查看单道题目 | Day 10 |
| POST | /questions | 创建一道题目 | Day 10 |
| PUT | /questions/{id} | 更新一道题目 | Day 10 |
| DELETE | /questions/{id} | 删除一道题目 | Day 10 |
| POST | /questions/detail | 创建带标签的题目（嵌套模型演示） | Day 9 |

**关键代码模式**：
```python
@app.get("/questions", response_model=ApiResponse)
def list_questions(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    # 1. 用 db 查询数据库
    # 2. 手动分页（切片）
    # 3. 用 ApiResponse 包装返回
```
- `response_model=ApiResponse` → 告诉 FastAPI 返回格式长什么样
- `Depends(get_db)` → 自动获取数据库会话，用完自动关闭

---

### 2. schemas/interview.py —— 数据校验模型

**作用**：定义"前端发来的 JSON 应该长什么样"和"后端返回的 JSON 长什么样"。

**包含 4 个模型**：

| 模型 | 用途 | 关键字段 |
|------|------|---------|
| QuestionCreate | 创建题目的请求体 | title, category, difficulty |
| QuestionResponse | 创建成功的响应体 | message, category, difficulty |
| Tag | 题目标签（小模型） | name |
| QuestionDetail | 带标签的题目详情 | title, category, difficulty, tags, answer |

**关键知识点**：
- `BaseModel` → 所有 Pydantic 模型的基类
- `Field(...)` → 定义字段约束（... 表示必填）
  - `min_length` / `max_length` → 字符串长度限制
  - `ge` / `le` → 数字范围限制（greater equal / less equal）
  - `default` → 默认值
  - `example` → Swagger 文档示例（不影响逻辑）
- `list[Tag]` → 嵌套模型，表示列表里每个元素都是 Tag 对象

---

### 3. schemas/response.py —— 统一响应格式

**作用**：所有接口都用同一个格式返回，前端只看 code 就知道成功还是失败。

**ApiResponse 结构**：
```json
{
    "code": 200,        // 状态码：200=成功，404=不存在
    "message": "success", // 提示信息
    "data": { ... }      // 实际数据（可以是任意类型）
}
```

**为什么需要统一响应**：
- 没有它：每个接口返回格式不一样，前端要写很多判断
- 有了它：前端只要 `if (response.code === 200)` 就够了

---

### 4. database.py —— 数据库连接配置

**作用**：让 FastAPI 能连接到 SQLite 数据库。

**包含 3 个核心零件**：

| 零件 | 类型 | 作用 |
|------|------|------|
| engine | 引擎 | 数据库连接器，负责和数据库通信 |
| SessionLocal | 会话工厂 | 每次调用创建一个会话（和数据库交互的窗口） |
| Base | 基类 | 所有数据库模型都要继承它 |
| get_db() | 函数 | 用 Depends 调用，创建会话 → 使用 → 自动关闭 |

**关键设置**：
```python
engine = create_engine(
    "sqlite:///./ai_interview.db",  # 数据库文件路径
    connect_args={"check_same_thread": False}  # SQLite 特有，允许 FastAPI 多线程访问
)
```

**get_db() 的工作方式**（yield 模式）：
```
调用 get_db()
    → 创建会话 db = SessionLocal()
    → yield db（暂停，把 db 交给接口函数使用）
    → 接口函数用完后，继续执行
    → db.close()（关闭会话）
```

---

### 5. models.py —— 数据库表结构

**作用**：定义数据库里有什么表、每张表有什么字段。

**Question 表结构**：

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | 主键，自增 | 唯一标识 |
| title | String(200) | 不能为空 | 题目标题 |
| category | String(50) | 不能为空 | 题目分类 |
| difficulty | Integer | 默认 3 | 难度等级 |

**和 schemas 的区别**：
- `models.py` 定义的是**数据库里存什么**（SQLAlchemy 模型）
- `schemas/` 定义的是**接口收发什么**（Pydantic 模型）
- 它们可以不一样！比如数据库有 id 字段，但创建题目时不需要传 id

---

### 6. logger.py —— 日志配置

**作用**：统一管理日志输出，方便调试和排查问题。

**双输出配置**：
- 控制台（StreamHandler）→ 级别 INFO，开发时看
- 文件（FileHandler）→ 级别 DEBUG，事后查

**日志格式**：
```
2025-01-01 12:00:00 | INFO     | ai_interview.main | 查看题目列表
```

**使用方式**：
```python
from app.logger import setup_logger
logger = setup_logger()
logger.info("普通信息")
logger.warning("警告")
logger.error("错误")
```

---

### 7. tests/test_questions.py —— 测试用例

**作用**：自动验证接口是否正常工作。

**包含 4 个测试**：

| 测试函数 | 测什么 |
|---------|--------|
| test_root | GET / 返回 200 + 包含"欢迎" |
| test_create_question | POST /questions 创建成功 |
| test_get_question | 创建后再 GET，能查到 |
| test_delete_question | 创建 → 删除 → 再查，返回 404 |

**运行方式**：
```bash
cd week2_fastapi
python -m pytest -v
```

---

## 数据流全景图

一次完整的"创建题目"请求，数据怎么流动：

```
前端发 POST 请求
    ↓
JSON: {"title": "什么是闭包？", "category": "Python", "difficulty": 3}
    ↓
FastAPI 收到请求
    ↓
Pydantic (QuestionCreate) 校验数据
    ↓ 不合格 → 返回 422 错误
Depends(get_db) 创建数据库会话
    ↓
SQLAlchemy (Question) 把 Python 对象写入 SQLite
    ↓
db.commit() 确认写入
    ↓
包装成 ApiResponse(code=200, message="创建成功", data={...})
    ↓
logger.info("创建题目：什么是闭包？")
    ↓
返回 JSON 给前端
```

---

## CRUD 是什么

CRUD 是四个英文单词的首字母缩写：

  C — Create（创建）
  R — Read（读取/查询）
  U — Update（更新）
  D — Delete（删除）

这四个操作是几乎所有后端系统的基础。不管什么业务系统，对数据的操作基本逃不出这四种。

类比通讯录 App：
  - 新建联系人（Create）
  - 查看联系人列表（Read）
  - 修改联系人电话（Update）
  - 删除联系人（Delete）

我们 Week 2 给"面试题"实现了这四个操作：
  - POST   /questions      → 创建一道题（Create）
  - GET    /questions      → 查看题目列表（Read）
  - PUT    /questions/{id} → 修改一道题（Update）
  - DELETE /questions/{id} → 删除一道题（Delete）

---

## Week 1 和 Week 2 的关联

```
Week 1：CLI 工具（本地运行，命令行交互）
    ↓ 升级
Week 2：后端服务（HTTP 接口，任何客户端都能调用）
```

对比：

| 维度 | Week 1 | Week 2 |
|------|--------|--------|
| 角色 | 调用方（调 DeepSeek API） | 被调用方（提供 API 给别人调） |
| 框架 | httpx | FastAPI |
| 数据存储 | 本地文件 history.json | SQLite 数据库 |
| 交互方式 | 命令行 | HTTP 接口 |
| 用户 | 只有自己 | 任何客户端（网页、App、其他服务） |

面试话术：

> "Week 1 我用 httpx 调用 DeepSeek API，学会了 HTTP 请求和异步编程。
> Week 2 我用 FastAPI 把它升级成了后端服务，从'调用方'变成了'被调用方'。
> 后面 Week 3 开始，我会在这个后端骨架上接入 LLM API，实现智能出题和评分，
> 这样前端用户发一道请求过来，后端就能自动用 AI 生成面试题。"

---

## 面试话术

### 版本 1：电梯演讲（30 秒）

> "我做了一个面试题管理后端服务，用 FastAPI + SQLAlchemy + SQLite 实现了完整的 CRUD 接口，支持分页查询和统一响应格式，还配了日志系统和自动化测试。"

适用场景：面试官问"简单介绍一下你的项目"，或者自我介绍时顺带提一下。

---

### 版本 2：标准版（2 分钟）

> "我用 FastAPI 搭建了一个面试题管理的后端服务，是 AI-Interview 智能模拟面试系统的后端骨架。
>
> **数据层**：用 Pydantic 定义请求和响应模型，前端发来的 JSON 会自动校验类型和约束，不合格直接返回 422 错误，不用手动写 if 判断。
>
> **业务层**：实现了题目的增删改查四个接口，还有分页查询。用统一的 ApiResponse 格式包装所有返回，前端只要判断 code 是不是 200 就行。
>
> **存储层**：用 SQLAlchemy ORM 连接 SQLite，不用写 SQL，Python 对象直接映射到数据库表。
>
> **工程化**：配了 logging 日志系统，控制台看 INFO 级别，文件记录 DEBUG 级别方便排查。测试用 pytest 的 TestClient，覆盖了创建、查询、删除的完整流程。"

适用场景：面试官问"详细介绍一下你的项目"，这是最常用的回答。

---

### 版本 3：技术深度版（追问时用）

如果面试官追问"具体用了什么技术"，展开讲：

**Q: 为什么用 FastAPI 而不是 Flask？**
> "FastAPI 有三个优势：第一，自动生成 Swagger 文档，前端可以直接在浏览器里测试接口；第二，内置 Pydantic 做数据校验，不用手动写验证逻辑；第三，原生支持异步，后续接入 LLM API 调用时性能更好。"

**Q: 什么是 ORM？为什么要用？**
> "ORM 是 Object-Relational Mapping，把数据库表映射成 Python 类。好处是不用写 SQL，用 Python 语法就能操作数据库。比如创建一条记录就是 `db.add(question)`，查询就是 `db.query(Question).all()`。如果以后换数据库（比如从 SQLite 换成 PostgreSQL），代码基本不用改。"

**Q: Depends(get_db) 是什么？**
> "这是 FastAPI 的依赖注入模式。get_db 是一个生成器函数，用 yield 创建数据库会话交给接口用，用完自动关闭。多个接口都依赖它，代码复用，而且会话管理不会遗漏。"

**Q: 你怎么测试的？**
> "用 pytest 配合 FastAPI 的 TestClient。TestClient 可以直接调用接口，不需要真正启动服务器。测试思路是先创建数据，再验证查询、修改、删除。比如删除测试：创建一道题 → 删除它 → 再查询确认返回 404。"

**Q: 项目有什么可以改进的地方？**
> "目前有几个可以优化的点：第一，加 JWT 认证，不是所有人都能操作题目；第二，把数据库从 SQLite 换成 PostgreSQL，生产环境更稳定；第三，加异步支持，用 async def 替代 def，提高并发性能；第四，加 Docker 容器化部署。"

---

### 版本 4：业务价值版（如果面试官问"这个项目有什么用"）

> "这是 AI-Interview 智能模拟面试系统的后端骨架。最终目标是实现一条完整链路：简历解析 → 岗位匹配 → RAG 出题 → AI 评分 → 面试报告。
>
> 我现在做的是最底层的题库管理服务，后续会在这个骨架上接入 LLM API 做智能出题和评分，接入向量数据库做题目检索，接入 Agent 做面试流程控制。FastAPI 作为后端框架，天然支持异步，后续接入这些 AI 能力很方便。"

---

## 面试高频 10 题

### Q1：介绍一下你的项目

> "我做了一个 AI-Interview 智能模拟面试系统，目前完成了后端骨架部分。用 FastAPI 搭建，Pydantic 做数据校验，SQLAlchemy ORM 连接 SQLite 做数据持久化，实现了面试题的增删改查和分页查询。所有接口统一用 ApiResponse 包装返回格式，配了 logging 日志系统和 pytest 自动化测试。后续会接入 LLM API 做智能出题和评分，接入 RAG 做题目检索，最终实现从简历解析到面试报告的完整闭环。"

**考察点**：表达能力、项目理解深度。不要背稿，用自己的话说。

---

### Q2：为什么用 FastAPI 而不是 Flask / Django？

> "选 FastAPI 有三个原因：第一，自动生成 Swagger 文档，开发阶段前端可以直接在浏览器测试接口，省去了写接口文档的时间；第二，内置 Pydantic 数据校验，请求参数不对直接返回 422，不用手写 if 判断；第三，原生支持 async/await 异步编程，后面接入 LLM API 时可以并发调用，性能更好。Django 太重，Flask 缺少这些内置能力。"

**考察点**：技术选型理由。面试官想听的是"你为什么选"，不是"它有什么功能"。

---

### Q3：什么是 RESTful API？

> "RESTful 是一种接口设计风格，核心是用 HTTP 方法表示操作类型：GET 查数据、POST 创建数据、PUT 修改数据、DELETE 删除数据。路径用名词表示资源，比如 /questions 表示题目集合，/questions/1 表示第 1 道题。好处是接口语义清晰，前端看路径和方法就知道在干什么，不用猜。"

**考察点**：后端基础概念。用你的项目举例会加分："我的项目就是按 RESTful 设计的，POST /questions 创建，GET /questions 查询。"

---

### Q4：GET 和 POST 有什么区别？

> "GET 是获取数据，参数放在 URL 里，比如 /questions?page=1，浏览器直接访问就能看到；POST 是提交数据，参数放在请求体（body）里，格式是 JSON，浏览器地址栏看不到。GET 请求是幂等的，查多少次结果一样；POST 不是幂等的，每发一次可能创建一条新数据。还有 GET 可以被浏览器缓存，POST 不会。"

**考察点**：HTTP 基础。这是最基础的问题，必须答清楚。

---

### Q5：Pydantic 是什么？你项目里怎么用的？

> "Pydantic 是 Python 的数据校验库，用类型注解定义数据结构，自动校验类型和约束。我项目里用它定义了请求模型和响应模型。比如 QuestionCreate 定义了 title 必须是字符串、长度 1-200、difficulty 必须是 1-5，前端发来的 JSON 不符合就自动返回 422 错误。FastAPI 内置集成了 Pydantic，接口函数的参数类型标注成 Pydantic 模型，FastAPI 就自动做校验和文档生成。"

**考察点**：数据校验理解。强调"自动校验"和"不用手写 if"是关键。

---

### Q6：什么是 ORM？SQLAlchemy 和直接写 SQL 有什么区别？

> "ORM 是 Object-Relational Mapping，把数据库表映射成 Python 类。我在 models.py 里定义了一个 Question 类，对应数据库的 questions 表，类的属性就是表的字段。操作数据库时用 Python 语法：db.add(question) 插入、db.query(Question).all() 查询，不用写 SQL。好处是代码可读性好、换数据库不用改代码。缺点是复杂查询不如原生 SQL 灵活，性能可能有损耗。"

**考察点**：数据库基础。如果面试官追问"什么时候该用原生 SQL"，回答："复杂联表查询、性能敏感的场景，可以用 SQLAlchemy 的 text() 执行原生 SQL。"

---

### Q7：Depends(get_db) 是什么？为什么这样写？

> "这是 FastAPI 的依赖注入模式。get_db 是一个生成器函数，用 yield 创建数据库会话交给接口函数使用，接口执行完后自动关闭会话。每个接口都需要数据库会话，如果不抽出来，每个接口都要写一遍创建和关闭的代码。用 Depends 注入后，代码复用，而且会话管理不会遗漏——就算接口报错了，finally 也会关闭会话，不会造成连接泄漏。"

**考察点**：设计模式理解。"依赖注入"这四个字要说出来。

---

### Q8：async / await 是什么？你项目里用了吗？

> "async/await 是 Python 的异步编程语法。async def 定义一个异步函数，遇到 await 时会暂停当前任务去做别的事，等结果回来再继续。我 Week 1 的项目里用 httpx.AsyncClient 并发调用 DeepSeek API，用 asyncio.gather 同时发多个请求，比串行快很多。Week 2 的 FastAPI 接口目前用的是同步（def），因为 CRUD 操作很快，不需要异步。但后面接入 LLM API 调用时会改成 async def，因为 LLM 响应慢，异步可以同时处理多个用户请求。"

**考察点**：异步编程理解。区分"什么时候需要异步"是加分项。

---

### Q9：你遇到过什么 Bug？怎么解决的？

> "我在做分页功能时遇到一个 Bug：计算了分页后的数据 paginated_data，但返回时写成了 data=questions（全量数据），分页做了白算。排查方法是看返回数据量，发现 page_size=1 但返回了全部数据，定位到返回变量名写错了。改成分页后的变量就好了。这个 Bug 教训是：变量名相似时容易搞混，写完要检查返回值是不是正确的那个变量。"

**考察点**：Debug 能力和反思能力。面试官想听你分析问题的过程，不是结果。

---

### Q10：项目下一步怎么规划？

> "后端骨架已经搭好了，下一步是接入 AI 能力。Week 3 会封装 LLM API Client，实现简历解析和岗位匹配；Week 4 接入向量数据库做面试题库 RAG 检索；Week 5 把匹配和检索组合起来做出题服务；Week 6-7 用 LangGraph 做 Agent 工作流，实现完整的面试流程控制；Week 8 工程化包装，Docker 部署、README、简历话术。最终目标是'简历进去、面试报告出来'的完整闭环。"

**考察点**：规划能力和项目完整性。展示你有清晰的路线图，不是做到哪算哪。
