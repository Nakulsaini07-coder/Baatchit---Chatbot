from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from .semantic_cache import query_cache, add_to_cache


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def make_chat_node(llm_with_tools):
    async def chat_node(state: ChatState, config=None):
        """LLM node that may answer or request a tool call."""
        thread_id = None
        if config and isinstance(config, dict):
            thread_id = config.get("configurable", {}).get("thread_id")

        system_message = SystemMessage(
            content=(
                "You are a helpful assistant. For questions about the uploaded PDF, call "
                "the `rag_tool` and include the thread_id "
                f"`{thread_id}`. You can also use the web search, stock price, and MCP "
                "tools when helpful. If no document is available, ask the user to upload "
                "a PDF."
            )
        )

        messages = [system_message, *state["messages"]]

        # Try semantic cache using the last user message as the query fingerprint.
        query_text = ""
        if state.get("messages"):
            # find last user message if available
            for m in reversed(state["messages"]):
                role = getattr(m, "role", None)
                if role == "user":
                    query_text = getattr(m, "content", "")
                    break
            if not query_text:
                # fallback to last message content
                last = state["messages"][-1]
                query_text = getattr(last, "content", "")

        if query_text:
            cached_resp, sim = query_cache(query_text)
            if cached_resp:
                ai_msg = AIMessage(content=cached_resp)
                return {"messages": [ai_msg]}

        response = await llm_with_tools.ainvoke(messages)

        # Add to semantic cache asynchronously (best-effort).
        try:
            # store using the last user query as key if available
            if query_text and getattr(response, "content", None):
                add_to_cache(query_text, getattr(response, "content"))
        except Exception:
            pass

        return {"messages": [response]}

    return chat_node


def build_chatbot(llm_with_tools, tools, checkpointer):
    graph = StateGraph(ChatState)
    graph.add_node("chat_node", make_chat_node(llm_with_tools))
    graph.add_edge(START, "chat_node")

    tool_node = ToolNode(tools) if tools else None
    if tool_node:
        graph.add_node("tools", tool_node)
        graph.add_conditional_edges("chat_node", tools_condition)
        graph.add_edge("tools", "chat_node")
    else:
        graph.add_edge("chat_node", END)

    return graph.compile(checkpointer=checkpointer)
