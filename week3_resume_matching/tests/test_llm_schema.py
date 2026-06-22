# 测试 chat_with_schema()：实际调用大模型，返回结构化数据

import asyncio
from app.config import load_config
from app.llm_client import DeepSeekClient
from app.prompts import RESUME_PARSE_PROMPT
from app.schemas.resume import ResumeInfo


async def main():
    # 第 1 步：加载配置，创建客户端
    config = load_config()
    client = DeepSeekClient(config)

    try:
        # 第 2 步：准备一段测试简历
        resume_text = """
        张三，男，25岁。
        教育背景：清华大学 计算机科学与技术 本科（2018-2022）
        技能：Python、Java、SQL、Git、FastAPI
        工作经历：2年 Python 后端开发
        项目经历：
        1. 开发了一个基于 FastAPI 的 RESTful API 服务
        2. 使用 SQLAlchemy 实现了用户管理系统
        """

        # 第 3 步：填入 Prompt 模板
        messages = [
            {"role": "user", "content": RESUME_PARSE_PROMPT.format(resume_text=resume_text)}
        ]

        # 第 4 步：调用大模型，用 Pydantic 校验结果
        print("正在调用大模型...")
        result = await client.chat_with_schema(messages, ResumeInfo)

        # 第 5 步：打印结果
        print(f"\n解析结果：")
        print(f"  姓名：{result.name}")
        print(f"  教育背景：{result.education}")
        print(f"  技能栈：{result.skills}")
        print(f"  工作年限：{result.experience_years}")
        print(f"  项目经历：{result.project_summary}")
        print(f"\n✅ 结构化输出测试通过！")

    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
