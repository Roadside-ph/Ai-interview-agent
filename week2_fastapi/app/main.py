"""AI-Interview Agent 后端服务入口。"""

from fastapi import FastAPI

# 创建 FastAPI 应用实例
# title 会显示在自动文档的标题里
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
