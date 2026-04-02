from __future__ import annotations

from typing import Optional

import requests
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool, tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from .pdf_index import get_retriever, thread_document_metadata

search_tool = DuckDuckGoSearchRun(region="us-en")


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA')
    using Alpha Vantage with API key in the URL.
    """
    url = (
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
        f"&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    )
    r = requests.get(url)
    return r.json()


@tool
def rag_tool(query: str, thread_id: Optional[str] = None) -> dict:
    """
    Retrieve relevant information from the uploaded PDF for this chat thread.
    Always include the thread_id when calling this tool.
    """
    retriever = get_retriever(thread_id)
    if retriever is None:
        return {
            "error": "No document indexed for this chat. Upload a PDF first.",
            "query": query,
        }

    result = retriever.invoke(query)
    context = [doc.page_content for doc in result]
    metadata = [doc.metadata for doc in result]

    return {
        "query": query,
        "context": context,
        "metadata": metadata,
        "source_file": thread_document_metadata(str(thread_id)).get("filename"),
    }


client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": "python",
            "args": ["mcp_serVer\\main.py"],
        },
        "expense": {
            "transport": "http",
            "url": "https://splendid-gold-dingo.fastmcp.app/mcp",
        },
    }
)


def load_mcp_tools(run_async_fn) -> list[BaseTool]:
    try:
        return run_async_fn(client.get_tools())
    except Exception:
        return []


def build_tools(llm, mcp_tools: list[BaseTool]):
    tools = [search_tool, get_stock_price, rag_tool, *mcp_tools]
    llm_with_tools = llm.bind_tools(tools) if tools else llm
    return tools, llm_with_tools
