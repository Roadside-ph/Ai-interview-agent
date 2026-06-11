# Week 1 - LLM CLI 调用工具

> AI Agent 实习冲刺 8 周课程 - Phase 1 项目
> 目标：上海/杭州 AI Agent 应用开发实习

## 项目简介

一个命令行 LLM 调用工具，封装 DeepSeek API，支持对话历史持久化、异步并发调用和 Rich 终端美化。作为 8 周 AI Agent 冲刺课程的第一个实战项目，重点训练 Python 工程基础、HTTP API 调用、异步编程和模块化设计。

## 项目结构

```
week1_llm_cli/
├── .env.example       # 配置模板（复制为 .env 后填入 API Key）
├── .gitignore         # Git 忽略规则
├── requirements.txt   # Python 依赖
├── README.md          # 项目说明
├── app/
│   ├── __init__.py    # 包标记
│   ├── main.py        # CLI 入口：交互式命令行对话（Rich 美化版）
│   ├── config.py      # 配置管理：从 .env 加载 API Key、Base URL 等
│   ├── history.py     # 对话历史持久化：JSON 文件的保存、读取、列表
│   ├── api_client.py  # 通用 HTTP 客户端：封装 httpx 的 GET/POST，含超时和异常处理
│   ├── llm_client.py  # LLM 客户端：封装 DeepSeek API 的 chat 调用（同步版）
│   ├── async_llm_client.py  # 异步 LLM 客户端：用 httpx.AsyncClient 并发调用
│   ├── timer.py       # 耗时统计装饰器：自动打印函数执行时间
│   ├── exceptions.py  # 自定义异常体系
│   └── logger.py      # 日志配置模块
├── tests/             # 测试目录
│   ├── test_exceptions.py      # 异常类继承测试
│   ├── test_logger.py          # 日志模块测试
│   ├── test_config.py          # 配置加载测试
│   ├── test_httpx.py           # httpx 基础测试
│   ├── test_llm.py             # LLM 调用测试
│   ├── test_async.py           # async/await 基础测试
│   ├── test_async_http.py      # 异步 HTTP 请求测试
│   ├── test_serial_vs_async.py # 串行 vs 并发速度对比
│   └── test_async_llm.py       # 异步 LLM 并发调用测试
└── data/              # 对话历史存储目录（已在 .gitignore 中排除）
```

## 技术栈

- Python 3.11+
- httpx - 异步/同步 HTTP 客户端
- python-dotenv - .env 配置管理
- rich - 终端美化输出（颜色、边框、动画）
- asyncio - Python 异步编程框架
- pytest - Python 测试框架
- logging - Python 内置日志模块
- DeepSeek API (deepseek-v4-pro) - LLM 服务

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/Roadside-ph/AI-agent.git
cd AI-agent

# 2. 创建虚拟环境并激活
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
# 编辑 .env，填入你的 DeepSeek API Key

# 5. 运行 CLI 工具
python -m app.main
```

## 使用方法

```
╭────────────────────────────────────────╮
│ LLM CLI 工具                           │
│ 输入问题，按回车发送。输入 quit 退出。 │
╰────────────────────────────────────────╯

>>> 你好
╭──── AI ─────────────────────────────╮
│ 你好！很高兴见到你～                 │
│ 有什么可以帮你的吗？                 │
╰─────────────────────────────────────╯

>>> quit
再见！

对话历史已保存到：data/20260610_123456.json
```

**退出方式**：
- 输入 `quit`、`exit` 或 `q`
- 按 Ctrl+C

**历史保存**：
- 退出时自动保存到 `data/` 目录
- JSON 格式，方便后续分析

## 模块说明

### main.py - CLI 入口
- 交互式命令行对话循环
- 用 Rich 美化终端输出（颜色、边框、动画）
- 支持 Ctrl+C 优雅退出
- 退出时自动保存对话历史

### config.py - 配置管理
- 使用 `@dataclass` 定义 `AppConfig` 数据类
- 从 `.env` 文件加载 API Key、Base URL、Model Name、History Dir
- 自动创建 history 目录，缺少 .env 时给出清晰报错

### history.py - 对话历史持久化
- `save_history()`: 将对话消息列表保存为 JSON 文件（按时间戳命名）
- `load_history()`: 从 JSON 文件读取对话历史
- `list_histories()`: 列出所有历史文件（按时间倒序）

### api_client.py - 通用 HTTP 客户端
- `APIClient` 类封装 httpx，支持 `with` 语句（上下文管理器）
- 统一的异常处理：超时、HTTP 状态码错误、网络错误
- 支持 GET/POST，自动拼接 base_url

### llm_client.py - LLM 客户端（同步版）
- `LLMClient` 基于 `APIClient` 封装 DeepSeek API 调用
- `chat()` 方法：传入消息列表，返回 AI 回复文本
- 使用 Bearer Token 认证

### async_llm_client.py - 异步 LLM 客户端
- `AsyncLLMClient` 基于 `httpx.AsyncClient` 封装异步 API 调用
- 支持 `async with` 自动关闭连接
- 可配合 `asyncio.gather()` 并发调用多个请求

### timer.py - 耗时统计装饰器
- `@timer` 装饰器自动打印函数执行时间
- 支持异步函数，用于对比串行和并发的速度差异

---

## 8 周学习计划总览

### Phase 1：Python 基础与后端骨架（Week 1-2）

| 周次 | 主题 | 核心产出物 | 状态 |
|------|------|-----------|------|
| Week 1 | Python MUP + HTTP + Git | LLM CLI 调用工具 | ✅ 已完成 |
| Week 2 | FastAPI 后端骨架 | Agent 后端服务骨架 | 未开始 |

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

---

## Week 1 详细进度

| Day | 内容 | 核心文件 | 状态 |
|-----|------|---------|------|
| Day 1 | Python 工程环境与函数基础 | config.py, history.py, .env | ✅ 已完成 |
| Day 2 | HTTP 与 API 调用 | api_client.py, test_httpx.py | ✅ 已完成 |
| Day 3 | 大模型 API 最小调用 | llm_client.py, test_llm.py | ✅ 已完成 |
| Day 4 | 异步实践，并发调用与耗时统计 | async_llm_client.py, timer.py | ✅ 已完成 |
| Day 5 | LLM CLI 工具搭建 | main.py | ✅ 已完成 |
| Day 6 | 代码重构与 Debug | exceptions.py, logger.py | ✅ 已完成 |
| Day 7 | 测试与复盘 | test_exceptions.py, test_logger.py, test_config.py | ✅ 已完成 |

### 已完成亮点

- **Day 1**: 用 dataclass 管理配置，用 dotenv 加载环境变量，实现了对话历史的 JSON 持久化
- **Day 2**: 封装了通用 APIClient，统一处理超时/HTTP错误/网络错误，支持 with 上下文管理
- **Day 3**: 基于 APIClient 封装 LLMClient，成功调用 DeepSeek API 获取回复
- **Day 4**: 学习异步编程（async/await），封装 AsyncLLMClient，实现并发调用 DeepSeek API，速度提升 2-3 倍
- **Day 5**: 搭建交互式 CLI 工具，集成 Rich 美化输出，支持对话历史持久化和优雅退出
- **Day 6**: 自定义异常体系（AppError/APIError/APITimeoutError/HttpError/NetworkError/ConfigError），logging 日志替代 print，代码重构提升可维护性
- **Day 7**: 学习 pytest 测试框架，编写 13 个单元测试覆盖异常、日志、配置模块，全部通过

---

## 最终目标项目

**AI-Interview：基于 RAG 与 Agent 的智能模拟面试系统**

完整业务链路：简历解析 -> 岗位匹配 -> RAG 出题 -> AI 评分 -> 面试报告

---

## 许可证

本项目为个人学习项目。
