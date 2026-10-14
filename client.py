import asyncio
from fastmcp import Client

client = Client("http://127.0.0.1:8006/mcp")

async def call_tool():
    async with client:
        result = await client.call_tool("greet", {"name": 'john'})
        print(result)

        response = await client.call_tool("web_search_tool", {"question": "what is rag?"})
        print(response)
        
        answer=await client.call_tool("rag_tools",{"question":"what is imobile?"})
        print(answer.content)


asyncio.run(call_tool())




