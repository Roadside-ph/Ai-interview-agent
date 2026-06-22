# 📅 Week 3：简历解析与岗位匹配

## 1. 核心技术拆解

### LLM API Client 封装

具体说明：

- 学什么：把 Week 1 的 `llm_client.py` 升级为生产级封装，支持重试、超时、流式输出、结构化输出
- 为什么对 Agent 开发重要：Agent 的每个 Tool 调用都需要稳定可靠的 LLM Client，封装不好会导致整个 Agent 不稳定
- 本周用在哪里：简历解析、JD 解析、岗位匹配都依赖 LLM Client 调用 DeepSeek API
- 常见错误认知：以为 LLM Client 就是"发个 HTTP 请求"，忽略了重试、超时、错误分类、成本控制
- 关联笔记：[[LLMClient 封装]]、[[DeepSeek API]]、[[异步 HTTP 客户端]]

### Prompt 模板管理

具体说明：

- 学什么：用 Pydantic 模型管理 Prompt 模板，支持变量注入、版本控制、多模板复用
- 为什么对 Agent 开发重要：Agent 的每个 Tool 都需要精心设计的 Prompt，模板化管理是工程化的基础
- 本周用在哪里：简历解析 Prompt、JD 解析 Prompt、岗位匹配 Prompt
- 常见错误认知：以为 Prompt 就是"写个字符串"，忽略了模板化、变量注入、版本管理
- 关联笔记：[[Prompt 模板管理]]、[[Pydantic 模型设计]]

### 结构化输出（Structured Output）

具体说明：

- 学什么：让 LLM 输出 JSON 格式，用 Pydantic 模型校验，处理 LLM 输出不稳定的坑
- 为什么对 Agent 开发重要：Agent 的 Tool 返回值必须是结构化数据，不能是自由文本
- 本周用在哪里：简历解析输出候选人画像、JD 解析输出岗位要求、匹配输出匹配度
- 常见错误认知：以为 LLM 会"乖乖输出 JSON"，实际上经常输出带 markdown 包裹的 JSON、多余字段、类型错误
- 关联笔记：[[结构化输出]]、[[JSON Schema]]、[[Pydantic 校验]]

### 流式输出（Streaming）

具体说明：

- 学什么：SSE（Server-Sent Events）流式输出，FastAPI 的 StreamingResponse
- 为什么对 Agent 开发重要：用户体验——等 10 秒才看到第一个字 vs 边生成边显示
- 本周用在哪里：简历解析结果实时展示、面试对话实时回复
- 常见错误认知：以为流式输出就是"分段发"，忽略了 SSE 协议格式、前端 EventSource 接收
- 关联笔记：[[SSE 流式输出]]、[[FastAPI StreamingResponse]]

## 2. 每日精细化学习路径

### Day 15：LLM API Client 封装

关联知识：[[LLMClient 封装]]、[[DeepSeek API]]、[[异步 HTTP 客户端]]、[[重试机制]]

学习内容：

- 回顾 Week 1 的 `llm_client.py`，分析不足
- 设计生产级 LLM Client：重试、超时、错误分类、日志
- 封装 `chat()` 方法支持普通调用和结构化输出
- 封装 `chat_stream()` 方法支持流式输出

今天写什么：

1. 创建 `app/llm_client.py`
2. 实现 `DeepSeekClient` 类
3. 支持 `chat()` 和 `chat_stream()` 方法
4. 加入重试装饰器和错误处理

验收标准：

- 能成功调用 DeepSeek API
- 网络错误时能自动重试
- 日志记录每次请求的耗时和状态

### Day 16：Prompt 模板 + 结构化输出

关联知识：[[Prompt 模板管理]]、[[结构化输出]]、[[Pydantic 校验]]、[[JSON Schema]]

学习内容：

- 设计 Prompt 模板管理方案
- 实现简历解析 Prompt、JD 解析 Prompt
- 让 LLM 输出 JSON 并用 Pydantic 校验
- 处理 LLM 输出不稳定的常见坑

今天写什么：

1. 创建 `app/prompts.py` 管理 Prompt 模板
2. 创建 `app/schemas/resume.py` 定义简历解析输出模型
3. 实现 `chat_with_schema()` 方法
4. 测试结构化输出的稳定性

验收标准：

- 能让 LLM 输出符合 Schema 的 JSON
- 能处理 LLM 输出的常见异常（多余字段、类型错误）
- Prompt 模板支持变量注入

### Day 17：简历解析接口

关联知识：[[简历解析]]、[[FastAPI 路由]]、[[文件上传]]、[[候选人画像]]

学习内容：

- 设计简历解析 API 接口
- 实现 PDF/Word 简历文本提取
- 调用 LLM 解析简历生成候选人画像
- 存储解析结果到数据库

今天写什么：

1. 创建 `app/routers/resume.py`
2. 实现 `POST /api/v1/resume/parse` 接口
3. 集成 LLM Client 和 Prompt 模板
4. 返回候选人画像 JSON

验收标准：

- 能上传简历文件并解析
- 解析结果包含教育背景、项目经历、技能栈
- 结果存入数据库

### Day 18：JD 解析 + 岗位匹配

关联知识：[[JD 解析]]、[[岗位匹配]]、[[匹配度计算]]、[[候选人画像]]

学习内容：

- 设计 JD 解析接口
- 实现岗位要求提取
- 设计岗位匹配算法（基于 LLM）
- 输出匹配度、优势、短板

今天写什么：

1. 创建 `app/routers/matching.py`
2. 实现 `POST /api/v1/matching/analyze` 接口
3. 调用 LLM 进行岗位匹配分析
4. 返回匹配结果 JSON

验收标准：

- 能输入 JD 文本并解析岗位要求
- 能与候选人画像进行匹配
- 输出匹配度、优势、短板、建议面试方向

### Day 19：流式输出 + 错误重试

关联知识：[[SSE 流式输出]]、[[FastAPI StreamingResponse]]、[[重试机制]]、[[错误处理]]

学习内容：

- 实现 SSE 流式输出
- FastAPI StreamingResponse 用法
- 前端 EventSource 接收
- 错误重试策略优化

今天写什么：

1. 实现 `GET /api/v1/resume/parse/stream` 流式接口
2. 修改 LLM Client 支持流式调用
3. 测试流式输出的用户体验
4. 优化重试策略

验收标准：

- 简历解析结果能实时流式展示
- 网络错误时能自动重试
- 流式输出格式符合 SSE 规范

### Day 20：测试 + 代码清理

关联知识：[[pytest 测试]]、[[FastAPI TestClient]]、[[Mock 测试]]、[[代码清理]]

学习内容：

- 给简历解析模块写测试
- 给岗位匹配模块写测试
- Mock LLM 调用
- 代码清理、日志完善

今天写什么：

1. 创建 `tests/test_resume.py`
2. 创建 `tests/test_matching.py`
3. Mock LLM Client 进行测试
4. 清理代码、补充日志

验收标准：

- 测试覆盖核心接口
- Mock LLM 调用避免真实 API 请求
- 代码符合 PEP 8 规范

### Day 21：复盘

关联知识：[[项目复盘]]、[[面试话术]]、[[AI-Interview 项目总览]]、[[简历解析与岗位匹配]]

学习内容：

- 生成 Week 3 复盘文档
- 整理面试话术
- 补充测试用例
- 更新 README

今天写什么：

1. 生成 `Week3复盘-项目结构.md`
2. 整理 4 个版本的面试话术
3. 补充边界测试用例
4. 更新 README.md
5. Git 提交 + 推送

验收标准：

- 复盘文档包含项目结构、数据流、面试话术
- 测试覆盖率达到 80%+
- README 反映最新状态

## 3. 本周核心产出物

### 项目名称：简历解析与岗位匹配 API

目录结构：

```
week3_resume_matching/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models.py            # 数据库模型
│   ├── llm_client.py        # LLM Client 封装
│   ├── prompts.py           # Prompt 模板管理
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── resume.py        # 简历解析接口
│   │   └── matching.py      # 岗位匹配接口
│   └── schemas/
│       ├── __init__.py
│       ├── resume.py        # 简历解析模型
│       ├── matching.py      # 岗位匹配模型
│       └── response.py      # 统一响应格式
├── tests/
│   ├── test_resume.py
│   └── test_matching.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

核心功能：

- 简历解析：上传 PDF/Word → 提取文本 → LLM 解析 → 候选人画像
- JD 解析：输入 JD 文本 → LLM 解析 → 岗位要求
- 岗位匹配：候选人画像 + 岗位要求 → LLM 匹配 → 匹配度 + 优势 + 短板

简历话术：

> 基于 FastAPI 和 DeepSeek API 实现简历解析与岗位匹配服务。使用 Pydantic 管理 Prompt 模板和结构化输出，支持 PDF/Word 简历上传、LLM 解析生成候选人画像、JD 解析提取岗位要求、智能岗位匹配分析。封装了生产级 LLM Client，支持重试、超时、流式输出。

面试可讲亮点：

- LLM Client 封装：重试机制、错误分类、日志记录
- 结构化输出：Pydantic Schema 校验 LLM 输出
- Prompt 模板管理：版本控制、变量注入、多模板复用
- 流式输出：SSE 实时展示解析结果

推荐建立的 Obsidian 笔记：

- [[AI-Interview 项目总览]]
- [[简历解析模块设计]]
- [[岗位匹配算法]]
- [[LLM 结构化输出]]

## 4. 面试仿真模拟

### Q1：你的简历解析模块是怎么实现的？

**标准回答**：

简历解析模块分为三步：首先是文件上传和文本提取，使用 PyPDF2 提取 PDF 文本，python-docx 提取 Word 文本。然后调用 DeepSeek API，通过精心设计的 Prompt 模板让 LLM 解析简历内容，提取教育背景、项目经历、技能栈等结构化信息。最后用 Pydantic 模型校验 LLM 输出的 JSON 格式，确保存入数据库的数据是规范的。

### Q2：LLM 输出不稳定怎么办？比如它输出的 JSON 格式不对。

**标准回答**：

这是生产环境中非常常见的问题。我的解决方案有三层：第一层是 Prompt 工程，在 Prompt 中明确指定 JSON Schema，给出示例；第二层是后处理，用正则提取 JSON 内容，处理 markdown 包裹、多余字段等问题；第三层是 Pydantic 校验，定义严格的模型，自动过滤多余字段、转换类型错误。如果三次重试后仍然失败，返回错误信息给用户。

### Q3：为什么选择用 LLM 做岗位匹配，而不是传统算法？

**标准回答**：

传统算法（如关键词匹配、TF-IDF）只能做表面匹配，无法理解语义。比如"熟悉 Python"和"3 年 Python 开发经验"，传统算法会认为是两个不同的技能。LLM 能理解语义相似性，还能给出匹配理由、优势分析、短板建议，这些是传统算法做不到的。当然，生产环境中可以结合两者：先用传统算法做粗筛，再用 LLM 做精细匹配，平衡成本和效果。

### Q4：你这个项目为什么不是普通 Demo？

**标准回答**：

这个项目有完整的业务闭环：简历解析 → 岗位匹配 → RAG 出题 → AI 评分 → 面试报告。不是单独的 RAG Demo 或 Agent Demo，而是把 RAG 和 Agent 整合到同一条业务链路中。工程化方面，使用 FastAPI 提供 RESTful API，SQLite 持久化数据，Pydantic 校验输入输出，pytest 测试覆盖核心模块。后续还会接入 RAG 检索面试题、Agent 编排面试流程，最终形成一个可投递的 AI Agent 项目。

## 5. 避坑指南

### LLM Client 封装

- **不要只做"发 HTTP 请求"**：生产级 Client 需要重试、超时、错误分类、日志、成本控制
- **不要忽略网络异常**：httpx 的 Timeout、ConnectError、HTTPStatusError 都要处理
- **不要硬编码 API Key**：使用 .env 管理敏感信息

### 结构化输出

- **不要相信 LLM 会"乖乖输出 JSON"**：必须做后处理和 Pydantic 校验
- **不要忽略 token 成本**：结构化输出会增加 token 消耗，需要控制 Prompt 长度
- **不要一次解析太长的简历**：分段解析，避免超出 LLM 上下文限制

### Prompt 模板

- **不要把 Prompt 写死在代码里**：用模板管理，方便版本控制和 A/B 测试
- **不要忽略 Prompt 版本**：每次修改 Prompt 都要记录版本，方便回滚
- **不要用太复杂的 Prompt**：简单清晰的 Prompt 效果更好

### 工程化

- **不要忘记更新 README.md**：每次提交代码前都要检查 README 是否反映最新状态
- **不要忘记测试**：至少覆盖核心接口的正常流程和异常流程
- **不要忘记 .gitignore**：排除 __pycache__/、venv/、.env、*.db、*.log、.pytest_cache/
