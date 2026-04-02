from __future__ import annotations

from .async_runtime import run_async, submit_async_task
from .checkpoint import init_checkpointer
from .graph import build_chatbot
from .llm_setup import llm
from .pdf_index import ingest_pdf, thread_document_metadata, thread_has_document
from .tools import build_tools, load_mcp_tools

mcp_tools = load_mcp_tools(run_async)
tools, llm_with_tools = build_tools(llm, mcp_tools)
checkpointer = run_async(init_checkpointer("chatbot.db"))
chatbot = build_chatbot(llm_with_tools, tools, checkpointer)


async def _alist_threads():
    all_threads = set()
    async for checkpoint in checkpointer.alist(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)


def retrieve_all_threads():
    return run_async(_alist_threads())


__all__ = [
    "chatbot",
    "ingest_pdf",
    "retrieve_all_threads",
    "submit_async_task",
    "thread_document_metadata",
    "thread_has_document",
]
