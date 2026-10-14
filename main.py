from fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchRun
from resources import rag_tool
import logging

mcp = FastMCP("My MCP Server")

@mcp.tool(name="greet")
def greet(name: str):
    return f"Hello, {name}!"

@mcp.tool(name="web_search_tool")
def web_search_tool(question:str):
    """Useful for searching information on the internet.use this current and factual information"""
    search=DuckDuckGoSearchRun()
    result=search.run(question)
    logging.info("web_search_tool called")
    return result

@mcp.tool(name="rag_tools",description="used the provided context to retrive answer")
def rag_tools(question:str):
    answer=rag_tool(question)
    logging.info("rag_tool called")
    return answer.strip()


if __name__ == "__main__":
    mcp.run(transport="http", port=8006)