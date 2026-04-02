from __future__ import annotations

import queue

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


def stream_assistant_response(chatbot, submit_async_task, user_input: str, thread_key: str):
    config = {
        "configurable": {"thread_id": thread_key},
        "metadata": {"thread_id": thread_key},
        "run_name": "chat_turn",
    }

    status_holder = {"box": None}

    def ai_only_stream():
        event_queue: queue.Queue = queue.Queue()

        async def run_stream():
            try:
                async for message_chunk, metadata in chatbot.astream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=config,
                    stream_mode="messages",
                ):
                    event_queue.put((message_chunk, metadata))
            except Exception as exc:
                event_queue.put(("error", exc))
            finally:
                event_queue.put(None)

        submit_async_task(run_stream())

        while True:
            item = event_queue.get()
            if item is None:
                break
            message_chunk, metadata = item
            if message_chunk == "error":
                raise metadata

            if isinstance(message_chunk, ToolMessage):
                tool_name = getattr(message_chunk, "name", "tool")
                if status_holder["box"] is None:
                    status_holder["box"] = st.status(
                        f"🔧 Using `{tool_name}` …", expanded=True
                    )
                else:
                    status_holder["box"].update(
                        label=f"🔧 Using `{tool_name}` …",
                        state="running",
                        expanded=True,
                    )

            if isinstance(message_chunk, AIMessage):
                yield message_chunk.content

    ai_message = st.write_stream(ai_only_stream())

    if status_holder["box"] is not None:
        status_holder["box"].update(
            label="✅ Tool finished", state="complete", expanded=False
        )

    return ai_message
