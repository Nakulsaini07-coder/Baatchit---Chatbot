from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage


def load_conversation(chatbot, thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    messages = state.values.get("messages", [])

    return [
        msg
        for msg in messages
        if isinstance(msg, HumanMessage)
        or (
            isinstance(msg, AIMessage)
            and bool(str(getattr(msg, "content", "")).strip())
            and not getattr(msg, "tool_calls", None)
        )
    ]


def to_message_history(messages):
    message_history = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            continue
        message_history.append({"role": role, "content": msg.content})
    return message_history
