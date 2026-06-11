"""LLM CLI 工具：交互式命令行对话（Rich 美化版）"""

import asyncio
from datetime import datetime
from app.config import load_config
from app.async_llm_client import AsyncLLMClient
from app.history import save_history


async def main():
    """主函数：交互式对话循环"""
    
    # 1. 读取配置
    config = load_config()
    
    # 2. 创建异步 LLM 客户端
    async with AsyncLLMClient(
        api_key=config.api_key,
        base_url=config.base_url,
        model=config.model_name,
    ) as client:
        
        # 导入 Rich（美化终端输出）
        from rich.console import Console
        from rich.panel import Panel
        from rich.markdown import Markdown
        
        console = Console()
        
        # 欢迎信息
        console.print(Panel.fit(
            "[bold green]LLM CLI 工具[/bold green]\n"
            "[dim]输入问题，按回车发送。输入 quit 退出。[/dim]",
            border_style="blue"
        ))
        
        messages = []  # 对话历史
        
        # 3. 交互循环
        while True:
            try:
                # 用户输入（用 Rich 颜色）
                console.print()
                user_input = console.input("[bold cyan]>>> [/bold cyan]").strip()
                
                # 检查退出命令
                if user_input.lower() in ["quit", "exit", "q"]:
                    console.print("[bold yellow]再见！[/bold yellow]")
                    break
                
                # 跳过空输入
                if not user_input:
                    continue
                
                # 添加用户消息到历史
                messages.append({"role": "user", "content": user_input})
                
                # 调用 LLM
                with console.status("[bold green]AI 思考中...[/bold green]"):
                    reply = await client.chat(messages)
                
                # 显示 AI 回复（用 Panel 框起来）
                console.print()
                console.print(Panel(
                    Markdown(reply),  # 支持 Markdown 格式
                    title="[bold blue]AI[/bold blue]",
                    border_style="blue",
                    padding=(1, 2)
                ))
                
                # 添加 AI 回复到历史
                messages.append({"role": "assistant", "content": reply})
                
            except KeyboardInterrupt:
                # Ctrl+C 优雅退出
                console.print("\n[bold yellow]再见！[/bold yellow]")
                break
        
        # 4. 退出时保存历史
        if messages:
            filepath = save_history(messages, config.history_dir)
            console.print(f"\n[dim]对话历史已保存到：{filepath}[/dim]")


# 启动程序
if __name__ == "__main__":
    asyncio.run(main())
