from __future__ import annotations

import streamlit as st

from backend.app import chatbot, retrieve_all_threads
from backend.async_runtime import submit_async_task
from backend.pdf_index import ingest_pdf, thread_document_metadata
from .conversation import load_conversation, to_message_history
from .state import ensure_session_state, reset_chat
from .streaming import stream_assistant_response


def _thread_label(thread_id, position: int) -> str:
    messages = load_conversation(chatbot, thread_id)
    history = to_message_history(messages)
    for item in history:
        if item.get("role") == "user":
            text = str(item.get("content", "")).strip().replace("\n", " ")
            if text:
                return text[:40] + ("..." if len(text) > 40 else "")
    return f"Chat {position}"


def run_app():
    thread_key, thread_docs, threads = ensure_session_state(retrieve_all_threads)
    selected_thread = None

    st.sidebar.title("Baatchit")

    if st.sidebar.button("New Chat"):
        reset_chat()
        st.rerun()

    if thread_docs:
        latest_doc = list(thread_docs.values())[-1]
        st.sidebar.success(
            f"Using `{latest_doc.get('filename')}` "
            f"({latest_doc.get('chunks')} chunks from {latest_doc.get('documents')} pages)"
        )
    else:
        st.sidebar.info("No PDF indexed yet.")

    uploaded_pdf = st.sidebar.file_uploader("Upload a PDF for this chat", type=["pdf"])
    if uploaded_pdf:
        if uploaded_pdf.name in thread_docs:
            st.sidebar.info(f"`{uploaded_pdf.name}` already processed for this chat.")
        else:
            with st.sidebar.status("Indexing PDF…", expanded=True) as status_box:
                summary = ingest_pdf(
                    uploaded_pdf.getvalue(),
                    thread_id=thread_key,
                    filename=uploaded_pdf.name,
                )
                thread_docs[uploaded_pdf.name] = summary
                status_box.update(
                    label="✅ PDF indexed", state="complete", expanded=False
                )

    st.sidebar.header("My Conversations")
    for idx, thread_id in enumerate(threads, start=1):
        label = _thread_label(thread_id, idx)
        if st.sidebar.button(label, key=f"side-thread-{thread_id}"):
            selected_thread = thread_id

    st.title("Baatchit")

    for message in st.session_state["message_history"]:
        with st.chat_message(message["role"]):
            st.text(message["content"])

    user_input = st.chat_input("Ask your query")

    if user_input:
        st.session_state["message_history"].append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.text(user_input)

        with st.chat_message("assistant"):
            ai_message = stream_assistant_response(
                chatbot=chatbot,
                submit_async_task=submit_async_task,
                user_input=user_input,
                thread_key=thread_key,
            )

        st.session_state["message_history"].append(
            {"role": "assistant", "content": ai_message}
        )

        doc_meta = thread_document_metadata(thread_key)
        if doc_meta:
            st.caption(
                f"Document indexed: {doc_meta.get('filename')} "
                f"(chunks: {doc_meta.get('chunks')}, pages: {doc_meta.get('documents')})"
            )

    st.divider()

    if selected_thread:
        st.session_state["thread_id"] = selected_thread
        messages = load_conversation(chatbot, selected_thread)
        st.session_state["message_history"] = to_message_history(messages)
        st.session_state["ingested_docs"].setdefault(str(selected_thread), {})
        st.rerun()
