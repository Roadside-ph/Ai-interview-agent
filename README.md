# AI-Interview Agent

> 8 周 AI Agent 实习冲刺项目
> 目标：上海/杭州 AI Agent 应用开发实习

## 项目总览

**最终目标**：AI-Interview —— 基于 RAG 与 Agent 的智能模拟面试系统

完整业务链路：简历解析 -> 岗位匹配 -> RAG 出题 -> AI 评分 -> 面试报告

## 学习路线

### Phase 1：Python 基础与后端骨架（Week 1-2）

| 周次 | 主题 | 核心产出物 | 状态 |
|------|------|-----------|------|
| Week 1 | Python MUP + HTTP + Git | LLM CLI 调用工具 | ✅ 已完成 |
| Week 2 | FastAPI 后端骨架 | Agent 后端服务骨架 | 进行中 |

### Phase 2：RAG 与 AI-Interview（Week 3-5）

| 周次 | 主题 | 核心产出物 | 状态 |
|------|------|-----------|------|
| Week 3 | 简历解析与岗位匹配 | 简历解析与岗位匹配 API | 未开始 |
| Week 4 | 面试题库 RAG v1 | 面试题库 RAG 检索服务 | 未开始 |
| Week 5 | 岗位匹配 + RAG 出题 v2 | 岗位匹配驱动的出题与评分服务 | 未开始 |

### Phase 3：Agent 与工作流（Week 6-7）

| 周次 | 主题 | 核心产出物 | 状态 |
|------|------|-----------|------|
| Week 6 | Agent 核心能力 | 岗位匹配 Agent 与面试流程 Agent | 未开始 |
| Week 7 | 主项目闭环 | AI-Interview 智能模拟面试系统 | 未开始 |

### Phase 4：工程化与面试冲刺（Week 8）

| 周次 | 主题 | 核心产出物 | 状态 |
|------|------|-----------|------|
| Week 8 | 工程化包装 + 面试准备 | 可展示项目 + 简历 + 面试题库 | 未开始 |

## 项目结构

```
ai-interview-agent/
├── week1_llm_cli/              # Week 1: LLM CLI 调用工具（已完成）
│   ├── app/                    # 源码（config, api_client, llm_client, async_llm_client, main）
│   ├── tests/                  # pytest 测试（13 个用例）
│   └── README.md
├── week2_fastapi/              # Week 2: FastAPI 后端骨架（进行中）
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI 入口，含 GET/POST 接口
│   │   │                      # GET /, GET /health
│   │   │                      # GET /questions, GET /questions/{id}
│   │   │                      # POST /questions, PUT /questions/{id}
│   │   │                      # DELETE /questions/{id}
│   │   └── schemas/           # Pydantic 数据模型
│   │       ├── __init__.py
│   │       ├── interview.py   # 面试题请求/响应/嵌套模型
│   │       └── response.py    # 统一响应格式 (ApiResponse)
│   ├── venv/                  # 虚拟环境（已 gitignore）
│   ├── requirements.txt
│   └── .gitignore
├── week3_*/                    # Week 3-8 待添加
└── README.md               # 本文件（总览）
```

## Week 1 详细进度

| Day | 内容 | 核心文件 | 状态 |
|-----|------|---------|------|
| Day 1 | Python 工程环境与函数基础 | config.py, history.py, .env | ✅ |
| Day 2 | HTTP 与 API 调用 | api_client.py | ✅ |
| Day 3 | 大模型 API 最小调用 | llm_client.py | ✅ |
| Day 4 | 异步实践，并发调用与耗时统计 | async_llm_client.py, timer.py | ✅ |
| Day 5 | LLM CLI 工具搭建 | main.py (Rich 美化) | ✅ |
| Day 6 | 代码重构与 Debug | exceptions.py, logger.py | ✅ |
| Day 7 | 测试与复盘 | test_exceptions.py, test_logger.py, test_config.py | ✅ |

## Week 2 详细进度

| Day | 内容 | 核心文件 | 状态 |
|-----|------|---------|------|
| Day 8 | FastAPI 项目结构与第一个接口 | main.py (GET /, GET /health) | ✅ |
| Day 9 | Pydantic 请求/响应模型 | schemas/interview.py (BaseModel, Field, 嵌套模型) | ✅ |
| Day 10 | CRUD 四件套 + 内存存储 | main.py (GET/PUT/DELETE /questions) | ✅ |
| Day 11 | 统一响应格式 + 分页 | main.py (ApiResponse, 分页参数) | ✅ |
| Day 12 | 数据库 ORM | 待做 | 待做 |
| Day 13 | 日志、配置、基础测试 | 待做 | 待做 |
| Day 14 | 复盘 | 待做 | 待做 |

## 技术栈

- **语言**：Python 3.11+
- **HTTP 客户端**：httpx
- **Web 框架**：FastAPI
- **数据校验**：Pydantic
- **ASGI 服务器**：uvicorn
- **配置管理**：python-dotenv
- **终端美化**：rich
- **异步编程**：asyncio
- **测试框架**：pytest
- **日志**：logging
- **LLM 服务**：DeepSeek API

## 快速开始

### Week 1: LLM CLI 工具

```bash
cd week1_llm_cli
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # 填入 API Key
python -m app.main
```

### Week 2: FastAPI 后端

```bash
cd week2_fastapi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# 浏览器打开 http://127.0.0.1:8000/docs
```

## 面试话术

> 这是我为期 8 周的 AI Agent 实习冲刺项目。从 Python 基础开始，逐步构建了一个完整的 AI-Interview 智能模拟面试系统。
>
> **Week 1** 我搭建了一个 LLM CLI 工具，封装了 DeepSeek API，支持异步并发调用、对话历史持久化、Rich 终端美化。学会了 HTTP 调用、异步编程、模块化设计、自定义异常和日志系统。
>
> **Week 2** 我用 FastAPI 把 CLI 工具升级成了后端服务，实现了 Pydantic 数据验证、JWT 认证、数据库 CRUD。
>
> 后续几周我会接入 RAG 检索、Agent 工作流，最终完成"简历解析 -> 岗位匹配 -> RAG 出题 -> AI 评分 -> 面试报告"的完整闭环。

## 许可证

本项目为个人学习项目。
