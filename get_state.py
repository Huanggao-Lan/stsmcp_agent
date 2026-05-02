import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # 使用 uv 的完整路径
    server_params = StdioServerParameters(
        command=r"C:\Users\Shinano\.local\bin\uv.exe",  # 完整路径
        args=[
            "run",
            "--directory",
            r"C:\Users\Shinano\Desktop\STSMCP\STS2MCP\mcp",
            "python",
            "server.py"
        ]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # 列出可用工具
            tools = await session.list_tools()
            print("=== 可用工具 ===")
            for tool in tools:
                # tool 是元组，直接用下标取值
                name = tool[0]
                description = tool[1]
                print(f"  - {name}: {description}")


            # 调用 get_game_state
            print("\n=== 获取游戏状态 ===")
            result = await session.call_tool("get_game_state", {})

            if result.content:
                for content_item in result.content:
                    if hasattr(content_item, 'text'):
                        try:
                            data = json.loads(content_item.text)
                            print(json.dumps(data, indent=2)[:2000])
                        except:
                            print(content_item.text[:2000])


if __name__ == "__main__":
    asyncio.run(main())