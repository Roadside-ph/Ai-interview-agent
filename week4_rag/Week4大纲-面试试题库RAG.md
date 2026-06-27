# 📅 Week 4：面试试题库 RAG v1

## 1. 核心技术拆解

### RAG（检索增强生成）

是什么：
- RAG = Retrieval-Augmented Generation，检索增强生成
- 先从知识库中检索相关内容，再把检索结果塞进 Prompt 让 LLM 回答
- 解决 LLM "幻觉"问题：不让 LLM 凭空编答案，而是基于真实数据回答

为什么对 AI-Interview 至关重要：
- 面试题库有几百上千道题，不可能全塞进 Prompt
- 需要根据"岗位"和"技能标签"精准检索相关题目
- 检索到的题目要带参考答案和关键评分点，供后续 AI 评分使用

本周用在哪里：
- 把面试题库导入向量数据库
- 根据候选人简历和目标岗位，语义检索最相关的面试题
- 返回题目 + 参考答案 + 引用来源

常见错误认知：
- ❌ "RAG 就是数据库查询" → RAG 是语义检索，不是 SQL 的精确匹配
- ❌ "Embedding 和 LLM 是同一个东西" → Embedding 只负责把文本变成数字向量，不生成文字
- ❌ "chunk 切得越小越好" → 太小会丢失上下文，太大会检索不准

关联笔记：[[RAG 检索增强生成]]、[[向量数据库]]、[[Embedding 模型]]

---

### Chroma 向量数据库

是什么：
- Chroma 是轻量级本地向量数据库，适合开发和原型阶段
- 核心操作：创建集合 → 插入文档 → 语义查询
- 数据自动持久化到本地目录

为什么先学 Chroma：
- 零配置，pip install 就能用
- 不需要 Docker 或云服务
- 后续可平滑迁移到 pgvector 或 Milvus

本周用在哪里：
- 存储面试题的向量表示
- 根据查询语句检索最相似的面试题

关联笔记：[[Chroma 向量数据库]]、[[向量检索原理]]

---

### LangChain 基础

是什么：
- LangChain 是 RAG/Agent 开发的主流框架
- 本周只用它的三个核心模块：DocumentLoader、TextSplitter、Retriever
- 不需要学 LangChain 的 Agent 和 Chain 部分（那是 Week 6 的事）

本周用在哪里：
- 加载面试题文档（JSON → Document）
- 切分长文本（RecursiveCharacterTextSplitter）
- 检索器封装（ChromaRetriever）

关联笔记：[[LangChain 基础]]、[[DocumentLoader]]、[[TextSplitter]]

---

## 2. 每日精细化学习路径

### Day 22：【概念普及】RAG 原理 + 题库数据准备

关联知识：[[RAG 检索增强生成]]、[[向量检索原理]]、[[面试题库数据模型]]

学习内容：
- RAG 的工作原理（检索 → 注入 Prompt → 生成）
- 面试题库的数据结构设计
- 准备面试题样本数据（JSON 格式）

今天写什么：
1. 创建 `data/questions.json` 面试题样本数据（20-30 道题）
2. 设计面试题数据结构（question, answer, key_points, tags, job_role）
3. 更新 `requirements.txt` 添加 week4 新依赖
4. 创建 `README.md` 项目说明

验收标准：
- 能画出 RAG 的数据流图（用户问题 → 向量检索 → 上下文注入 → LLM 回答）
- 能解释"为什么不能把所有题目塞进 Prompt"
- 面试题 JSON 文件格式正确，包含至少 20 道题

---

### Day 23：【实操】LangChain 文档加载与文本切分

关联知识：[[LangChain DocumentLoader]]、[[TextSplitter]]、[[chunk_size 调优]]

学习内容：
- LangChain Document 对象
- JSONLoader 加载面试题
- RecursiveCharacterTextSplitter 切分策略
- chunk_size 和 chunk_overlap 的含义

今天写什么：
1. 安装 langchain、langchain-community
2. 写 `app/data_loader.py`：加载 questions.json → Document 对象
3. 写 `app/text_splitter.py`：切分文档，观察不同 chunk_size 的效果
4. 打印切分结果，理解 chunk 的含义

验收标准：
- 能解释 Document 对象的 page_content 和 metadata
- 能解释 chunk_size=500 和 chunk_size=1000 的区别
- 切分后的 chunk 数量和内容符合预期

---

### Day 24：【实操】Embedding + Chroma 向量入库

关联知识：[[Embedding 模型]]、[[Chroma 向量数据库]]、[[向量相似度]]

学习内容：
- Embedding 的概念（文本 → 数字向量）
- 使用 Embedding 模型（OpenAI-compatible 或本地模型）
- Chroma 基本操作：创建集合、插入、查询
- 余弦相似度

今天写什么：
1. 安装 chromadb
2. 写 `app/embedder.py`：封装 Embedding 调用
3. 写 `app/vector_store.py`：创建 Chroma 集合，插入面试题
4. 测试：查询"Python 异步编程"，返回最相似的 3 道题

验收标准：
- 能解释 Embedding 向量是什么（一串数字，表示文本的"含义"）
- 能解释为什么语义相似的文本，向量距离也近
- Chroma 查询返回结果与查询语义相关

---

### Day 25：【实操】RAG 检索链路搭建

关联知识：[[RAG Retriever]]、[[Prompt 注入检索结果]]、[[引用来源]]

学习内容：
- LangChain Retriever 接口
- 将检索结果格式化为 Prompt 上下文
- 调用 LLM 生成回答
- 返回引用来源（哪些题目被检索到）

今天写什么：
1. 写 `app/retriever.py`：封装 Chroma 检索器
2. 写 `app/rag_chain.py`：检索 → 格式化上下文 → 调用 LLM
3. 测试：输入"Python 装饰器"，返回相关题目 + LLM 解析
4. 输出中包含引用来源（题目 ID）

验收标准：
- 能解释 RAG 的完整流程（Query → Embedding → 检索 → Prompt → LLM → 回答）
- 检索结果与查询语义相关
- 回答中引用了检索到的题目

---

### Day 26：【服务化】面试试题库 RAG API 接口

关联知识：[[FastAPI RAG 路由]]、[[APIRouter]]、[[岗位标签筛选]]

学习内容：
- 将 RAG 链路封装为 FastAPI 接口
- 支持按岗位/技能标签筛选
- 返回结构化响应（题目列表 + 引用来源）
- 与 Week 3 的简历解析/岗位匹配对接

今天写什么：
1. 写 `app/schemas/rag.py`：RAG 相关 Pydantic 模型
2. 写 `app/routers/rag.py`：RAG 检索路由
3. 接口 1：`POST /rag/search` — 语义检索面试题
4. 接口 2：`POST /rag/search-by-job` — 按岗位 + 语义混合检索
5. 更新 `app/main.py` 注册路由

验收标准：
- Swagger UI 能正常调用两个接口
- 返回结果包含题目、参考答案、关键评分点、引用来源
- 按岗位筛选时，结果更精准

---

### Day 27：【测试 + 清理】RAG 测试与代码清理

关联知识：[[RAG 测试策略]]、[[Mock Embedding]]、[[检索质量评估]]

学习内容：
- RAG 测试策略（检索相关性、响应格式、异常处理）
- Mock Embedding 和 Chroma 进行单元测试
- 代码清理和文档更新

今天写什么：
1. 写 `tests/test_rag.py`：RAG 接口测试
2. 测试场景：正常检索、空结果、无效输入、按岗位筛选
3. 更新 requirements.txt
4. 更新 README.md

验收标准：
- 测试用例覆盖核心场景
- requirements.txt 包含所有新增依赖
- README 反映最新进度

---

### Day 28：【复盘】Week 4 复盘与面试话术

关联知识：[[RAG 面试表达]]、[[AI-Interview 项目总览]]、[[向量检索面试题]]

学习内容：
- 项目结构回顾
- RAG 核心概念复习
- 面试话术整理
- 高频面试题准备

今天写什么：
1. 生成 `Week4复盘-面试试题库RAG.md`
2. 项目结构总览 + 数据流全景图
3. 面试话术（4 个版本）
4. 高频面试题（10 道）
5. Git commit + push

验收标准：
- 能用 2 分钟讲清 RAG 在 AI-Interview 中的作用
- 能解释"为什么不直接用 SQL 查询面试题"
- 复盘文档完整

---

## 3. 本周核心产出物

### 项目名称：面试试题库 RAG 检索服务 v1

目标目录结构：
```
week4_rag/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口（注册 RAG 路由）
│   ├── config.py             # 配置管理
│   ├── database.py           # 数据库配置
│   ├── models.py             # 数据库模型
│   ├── exceptions.py         # 自定义异常
│   ├── logger.py             # 日志配置
│   ├── llm_client.py         # DeepSeek 客户端
│   ├── data_loader.py        # 面试题数据加载（新增）
│   ├── text_splitter.py      # 文本切分（新增）
│   ├── embedder.py           # Embedding 封装（新增）
│   ├── vector_store.py       # Chroma 向量存储（新增）
│   ├── retriever.py          # 检索器封装（新增）
│   ├── rag_chain.py          # RAG 链路（新增）
│   ├── prompts.py            # Prompt 模板（更新）
│   ├── schemas/              # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── rag.py            # RAG 相关 schema（新增）
│   │   ├── response.py       # 统一响应格式
│   │   └── resume.py         # 简历 schema
│   └── routers/              # API 路由
│       ├── __init__.py
│       ├── rag.py            # RAG 检索路由（新增）
│       ├── resume.py         # 简历解析路由
│       └── match.py          # 岗位匹配路由
├── data/
│   └── questions.json        # 面试题样本数据（新增）
├── tests/
│   ├── test_rag.py           # RAG 测试（新增）
│   └── ...                   # 从 week3 继承的测试
├── requirements.txt          # 更新依赖
├── .env.example
├── .gitignore
└── README.md                 # 项目说明（新增）
```

核心功能：
- 面试题数据加载与向量化
- 语义检索面试题
- 按岗位/技能标签筛选
- RAG 问答（检索 + LLM 生成）
- 返回引用来源

简历话术：
> 基于 RAG 技术构建面试题库检索服务，使用 Chroma 向量数据库存储面试题向量，支持语义检索和岗位标签筛选，将检索结果注入 LLM Prompt 生成结构化面试问答，为 AI-Interview 系统提供精准的题目检索能力。

面试可讲亮点：
- RAG 解决了 LLM 幻觉问题，让回答基于真实题库
- 向量检索 vs SQL 查询的权衡（语义理解 vs 精确匹配）
- chunk_size 调优经验
- Chroma 本地部署 vs 云服务的选择

推荐建立的 Obsidian 笔记：
- [[AI-Interview 项目总览]]
- [[面试题库 RAG]]
- [[RAG 检索增强生成]]
- [[Chroma 向量数据库]]
- [[Embedding 模型]]

---

## 4. 面试仿真模拟

**Q1：什么是 RAG？为什么你的项目需要 RAG？**

> RAG 是检索增强生成，先从知识库检索相关内容，再把结果注入 Prompt 让 LLM 回答。我的项目用 RAG 是因为面试题库有几百道题，不可能全塞进 Prompt，需要根据岗位和技能精准检索。

**Q2：为什么不直接用 SQL 查询面试题，而要用向量检索？**

> SQL 是精确匹配，用户搜"Python 异步"只能匹配包含这几个字的题目。向量检索是语义匹配，搜"Python 异步"也能找到"asyncio"、"协程"、"并发"相关的题目。面试场景下，候选人的问题描述往往不精确，语义检索更灵活。

**Q3：什么是 Embedding？它和 LLM 有什么区别？**

> Embedding 是把文本变成一串数字（向量），这串数字表示文本的"含义"。LLM 是生成文字的，Embedding 是把文字变成数字的。RAG 中，Embedding 负责把题目和查询都变成向量，然后用向量距离找最相似的题目。

**Q4：chunk_size 怎么选？太大或太小有什么问题？**

> chunk_size 太小（如 100），每个 chunk 信息不完整，检索到的内容缺上下文。太大（如 2000），检索精度下降，可能匹配到不相关的内容。面试题场景下，每道题通常 200-500 字，所以 chunk_size 设为 500 左右比较合适。

**Q5：你这个项目为什么不是普通 Demo？**

> 普通 Demo 只展示"能检索"，我的项目把 RAG 嵌入了完整业务链路：简历解析 → 岗位匹配 → RAG 出题 → AI 评分 → 面试报告。RAG 不是孤立功能，而是为"精准出题"和"有依据评分"服务的。而且有 FastAPI 服务化、数据库持久化、测试覆盖、Docker 部署说明。

**Q6：Chroma 和 pgvector 有什么区别？什么时候该换？**

> Chroma 是轻量级本地向量库，适合原型开发，零配置。pgvector 是 PostgreSQL 的向量扩展，适合生产环境，支持 SQL + 向量混合查询。当数据量超过 10 万条、需要多用户并发访问、或者需要和业务数据联合查询时，应该换 pgvector。

---

## 5. 避坑指南

1. **不要做孤立的 RAG Demo**：RAG 必须服务于面试题库检索，最终要能对接简历解析和岗位匹配，形成业务闭环。

2. **不要忽略 Embedding 成本**：每次入库都要调 Embedding API，几百道题可能花几块钱。先用小数据集测试，确认没问题再批量入库。

3. **chunk 不是越小越好**：面试题通常是一整道题 + 答案，不要把一道题切成多个 chunk，会破坏语义完整性。

4. **metadata 很重要**：入库时要把岗位标签、技能标签、题目 ID 存到 metadata 里，方便后续按标签筛选。

5. **测试要 Mock Embedding 和 Chroma**：单元测试不要真的调 Embedding API 和 Chroma，用 Mock 替代，否则测试慢且不稳定。

6. **requirements.txt 要补全**：新增 langchain、chromadb、langchain-community 等依赖，不要漏掉。

7. **README 要更新**：每次提交前检查 README 是否反映了最新进度。Week 4 状态改为"进行中"。
