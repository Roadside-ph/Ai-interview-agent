# Week 4: 面试题库 RAG v1

> 基于 RAG 技术的面试题库检索服务

## 核心功能

- 面试题数据加载与向量化
- 语义检索面试题（向量相似度匹配）
- 按岗位/技能标签筛选
- RAG 问答（检索 + LLM 生成）
- 返回引用来源

## 技术栈

- **Web 框架**：FastAPI
- **向量数据库**：Chroma
- **RAG 框架**：LangChain
- **Embedding**：sentence-transformers
- **LLM**：DeepSeek API
- **数据库**：SQLite（题目元数据）

## 项目结构

```
week4_rag/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py             # 配置管理
│   ├── database.py           # 数据库配置
│   ├── models.py             # 数据库模型
│   ├── exceptions.py         # 自定义异常
│   ├── logger.py             # 日志配置
│   ├── llm_client.py         # DeepSeek 客户端
│   ├── prompts.py            # Prompt 模板
│   ├── data_loader.py        # 面试题数据加载（待创建）
│   ├── text_splitter.py      # 文本切分（待创建）
│   ├── embedder.py           # Embedding 封装（待创建）
│   ├── vector_store.py       # Chroma 向量存储（待创建）
│   ├── retriever.py          # 检索器封装（待创建）
│   ├── rag_chain.py          # RAG 链路（待创建）
│   ├── schemas/              # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── rag.py            # RAG 相关 schema（待创建）
│   │   ├── response.py       # 统一响应格式
│   │   └── resume.py         # 简历 schema
│   └── routers/              # API 路由
│       ├── __init__.py
│       ├── rag.py            # RAG 检索路由（待创建）
│       ├── resume.py         # 简历解析路由
│       └── match.py          # 岗位匹配路由
├── data/
│   └── questions.json        # 面试题样本数据（20 道）
├── tests/
│   ├── test_rag.py           # RAG 测试（待创建）
│   └── ...                   # 从 week3 继承的测试
├── requirements.txt
├── .env.example
└── .gitignore
```

## 快速开始

```bash
cd week4_rag
conda activate ai-agent
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# 浏览器打开 http://127.0.0.1:8000/docs
```

## 学习进度

| Day | 内容                         | 核心文件                              | 状态 |
|-----|------------------------------|---------------------------------------|------|
| 22  | RAG 概念普及 + 题库数据准备  | data/questions.json                   | 待做 |
| 23  | LangChain 文档加载与文本切分 | data_loader.py, text_splitter.py      | 待做 |
| 24  | Embedding + Chroma 向量入库  | embedder.py, vector_store.py          | 待做 |
| 25  | RAG 检索链路搭建             | retriever.py, rag_chain.py            | 待做 |
| 26  | 面试题库 RAG API 接口        | routers/rag.py, schemas/rag.py        | 待做 |
| 27  | 测试 + 代码清理              | tests/test_rag.py                     | 待做 |
| 28  | 复盘                         | Week4复盘-面试试题库RAG.md            | 待做 |
