from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


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
        response = await llm_with_tools.ainvoke(messages)
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
