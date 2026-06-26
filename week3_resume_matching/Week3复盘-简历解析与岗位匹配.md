# Week 3 复盘 - 简历解析与岗位匹配

## 项目结构总览

```
week3_resume_matching/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口，注册路由
│   ├── config.py            # 配置管理（从 .env 读取）
│   ├── database.py          # 数据库连接配置（SQLAlchemy）
│   ├── models.py            # 数据库模型（Question 表）
│   ├── exceptions.py        # 自定义异常类
│   ├── logger.py            # 日志配置
│   ├── llm_client.py        # DeepSeek API 客户端（支持重试、流式输出）
│   ├── prompts.py           # Prompt 模板（简历解析、JD 解析、岗位匹配）
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── interview.py     # 面试题 Pydantic 模型
│   │   ├── response.py      # 统一响应格式 ApiResponse
│   │   └── resume.py        # 简历/岗位/匹配结果 Pydantic 模型
│   └── routers/
│       ├── __init__.py
│       ├── resume.py        # /resume/parse 接口
│       ├── match.py         # /matching/parse-jd、/matching/match 接口
│       └── stream.py        # /stream/chat 流式输出接口
├── tests/
│   ├── test_questions.py    # Week 2 CRUD 接口测试
│   ├── test_llm_client.py   # LLM Client 测试
│   ├── test_llm_schema.py   # 结构化输出测试
│   ├── test_prompt_schema.py # Prompt 模板测试
│   ├── test_stream.py       # 流式输出测试
│   ├── test_resume.py       # 简历解析接口测试（Day 20 新增）
│   └── test_match.py        # 岗位匹配接口测试（Day 20 新增）
├── data/                    # 数据文件
├── requirements.txt
├── .env                     # 环境变量（API Key 等）
├── .env.example             # 环境变量示例
└── .gitignore
```

## 文件依赖关系

```
main.py
├── routers/resume.py
│   ├── schemas/resume.py (ResumeInfo)
│   ├── schemas/response.py (ApiResponse)
│   ├── prompts.py (RESUME_PARSE_PROMPT)
│   ├── llm_client.py (DeepSeekClient)
│   └── config.py (load_config)
├── routers/match.py
│   ├── schemas/resume.py (JobInfo, MatchResult)
│   ├── schemas/response.py (ApiResponse)
│   ├── prompts.py (JD_PARSE_PROMPT, MATCHING_PROMPT)
│   ├── llm_client.py (DeepSeekClient)
│   └── config.py (load_config)
└── routers/stream.py
    ├── llm_client.py (DeepSeekClient)
    └── config.py (load_config)
```

## 数据流全景图

### 简历解析流程

```
用户发送简历文本
    ↓
POST /resume/parse
    ↓
routers/resume.py
    ↓
prompts.py (RESUME_PARSE_PROMPT.format(resume_text=...))
    ↓
llm_client.py (chat_with_schema)
    ↓
DeepSeek API
    ↓
返回 JSON → Pydantic 校验 (ResumeInfo)
    ↓
ApiResponse(code=200, data=...)
    ↓
返回给用户
```

### 岗位匹配流程

```
用户发送简历信息 + JD 信息
    ↓
POST /matching/match
    ↓
routers/match.py
    ↓
prompts.py (MATCHING_PROMPT.format(...))
    ↓
llm_client.py (chat_with_schema)
    ↓
DeepSeek API
    ↓
返回 JSON → Pydantic 校验 (MatchResult)
    ↓
ApiResponse(code=200, data=...)
    ↓
返回给用户
```

## 核心概念解释

### 1. Pydantic 模型（数据质检员）

类比：快递站的质检员，检查包裹是否符合规格。

```python
class ResumeInfo(BaseModel):
    name: str | None = None          # 姓名（可选）
    education: list[str] | None = []  # 学历列表（可选）
    skills: list[str] | None = []     # 技能列表（可选）
    experience_years: int | None = None  # 工作年限（可选）
    project_summary: list[str] | None = []  # 项目经历（可选）
```

作用：确保大模型返回的数据格式正确，字段类型匹配。

### 2. APIRouter（子路由器）

类比：餐厅的不同窗口（点餐窗口、结账窗口）。

```python
router = APIRouter(prefix="/resume", tags=["简历解析"])
```

- `prefix="/resume"`：所有接口路径以 `/resume` 开头
- `tags=["简历解析"]`：Swagger 文档中的分类标签

### 3. Mock 测试（假装调用）

类比：测试服务员时，用假厨房代替真厨房。

```python
@patch("app.routers.resume.DeepSeekClient")
def test_parse_resume_success(MockClient):
    mock_instance = MockClient.return_value
    mock_instance.chat_with_schema = AsyncMock(return_value=MOCK_DATA)
    # 测试时不会真的调用 DeepSeek API
```

作用：测试时不消耗 API 额度，测试速度快，结果稳定。

### 4. 异常处理（try-except-finally）

类比：餐厅厨房着火时，服务员告诉顾客"抱歉，厨房出了点问题"。

```python
try:
    result = await client.chat_with_schema(...)
    return ApiResponse(code=200, ...)
except Exception as e:
    return ApiResponse(code=500, message=f"失败：{str(e)}")
finally:
    await client.aclose()  # 无论成功失败，都关闭连接
```

作用：捕获异常，返回友好错误信息，确保资源释放。

## 面试话术

### 电梯演讲（30 秒）

> 我用 FastAPI 和 DeepSeek API 搭建了一个简历解析与岗位匹配系统。用户发送简历文本，系统调用大模型提取结构化信息（姓名、学历、技能、工作年限），然后和岗位要求进行匹配分析，返回匹配度、优势、劣势和面试建议。技术栈包括 FastAPI、Pydantic、SQLAlchemy、httpx。

### 标准版（2 分钟）

> 这是我的 AI Agent 实习冲刺项目的第三周成果。我实现了一个完整的简历解析与岗位匹配 API。
>
> **简历解析**：用户发送简历文本，系统通过 Prompt 模板将文本发送给 DeepSeek API，大模型返回 JSON 格式的结构化信息，我用 Pydantic 模型进行校验，确保数据格式正确。
>
> **岗位匹配**：用户发送简历信息和岗位描述，系统分析两者的匹配度，返回匹配分数、优势、劣势和面试建议。
>
> **技术亮点**：
> 1. 使用 Pydantic 进行数据校验，确保大模型返回的数据格式正确
> 2. 使用 APIRouter 进行路由拆分，代码结构清晰
> 3. 使用 Mock 进行单元测试，测试覆盖率高
> 4. 使用 try-except-finally 进行异常处理，确保资源释放
>
> **测试覆盖**：13 个测试用例，覆盖接口能通、数据逻辑、边界情况三个层次。

### 技术深度版（追问版）

> **Q: 为什么用 Pydantic 而不是直接用 dict？**
> A: Pydantic 提供数据校验和类型提示。如果大模型返回的数据格式错误（比如 `experience_years` 返回了字符串），Pydantic 会抛出异常，而不是让错误数据流入下游。
>
> **Q: 为什么要 Mock 测试？**
> A: 测试时不消耗 API 额度，测试速度快（毫秒级 vs 几秒），结果稳定（固定返回 vs 每次不同）。
>
> **Q: 异常处理为什么用 finally？**
> A: finally 里的代码无论成功失败都会执行。把 `client.aclose()` 放在 finally 里，确保网络连接一定会被释放，不会占用资源。
>
> **Q: 为什么用 APIRouter 而不是直接在 main.py 里写接口？**
> A: 路由拆分让代码结构清晰，每个文件负责一个功能模块，便于维护和扩展。

### 业务价值版

> 这个系统解决的核心问题是：**HR 筛选简历效率低**。
>
> 传统方式：HR 手动阅读简历，提取关键信息，和岗位要求对比，每份简历需要 3-5 分钟。
>
> 使用这个系统：发送简历文本，1 秒内返回结构化信息和匹配分析，HR 只需要看结果。
>
> **价值**：
> 1. 效率提升：从 3-5 分钟/份 → 1 秒/份
> 2. 标准化：统一的分析标准，避免主观偏差
> 3. 可扩展：可以批量处理，支持大规模招聘

## 高频面试题（10 道）

### 1. 介绍一下你的项目

**答案**：这是一个基于 FastAPI 和 DeepSeek API 的简历解析与岗位匹配系统。用户发送简历文本，系统调用大模型提取结构化信息，然后和岗位要求进行匹配分析。

### 2. 为什么选择 FastAPI？

**答案**：
1. 自动生成 API 文档（Swagger UI）
2. 支持异步编程（async/await）
3. 使用 Pydantic 进行数据校验
4. 性能好（基于 Starlette）

### 3. 什么是 Pydantic？

**答案**：Pydantic 是一个数据校验库，通过定义 Python 类来声明数据格式。如果数据格式错误，会抛出异常。类似快递站的质检员，检查包裹是否符合规格。

### 4. 为什么要 Mock 测试？

**答案**：
1. 不消耗 API 额度
2. 测试速度快（毫秒级）
3. 结果稳定（固定返回）
4. 可以模拟各种异常情况

### 5. 解释一下 try-except-finally

**答案**：
- `try`：尝试执行可能出错的代码
- `except`：如果出错，执行这里的代码
- `finally`：无论成功失败，都会执行这里的代码（通常用于资源释放）

### 6. 什么是 APIRouter？

**答案**：APIRouter 是 FastAPI 的路由分组工具。类比餐厅的不同窗口（点餐窗口、结账窗口），每个窗口负责不同的功能。使用 APIRouter 可以让代码结构清晰，便于维护。

### 7. 为什么用 DeepSeek API？

**答案**：
1. 支持中文
2. 价格便宜
3. 性能好
4. 兼容 OpenAI API 格式

### 8. 如何处理大模型返回的数据？

**答案**：
1. 大模型返回 JSON 字符串
2. 用 Pydantic 模型进行校验
3. 如果格式正确，返回结构化数据
4. 如果格式错误，抛出异常

### 9. 你的测试覆盖率是多少？

**答案**：13 个测试用例，覆盖三个层次：
1. 接口能通（HTTP 状态码正确）
2. 数据逻辑对（创建后再查询，数据一致）
3. 边界情况（空文本、模拟 API 报错）

### 10. 这个项目有什么可以改进的地方？

**答案**：
1. 添加用户认证（JWT）
2. 使用缓存（Redis）减少重复调用
3. 添加日志记录，方便排查问题
4. 使用 Docker 部署，方便扩展
5. 添加批量处理功能，支持大规模招聘
