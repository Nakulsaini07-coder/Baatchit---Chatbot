from __future__ import annotations

import uuid

import streamlit as st


def generate_thread_id():
    return uuid.uuid4()


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []


def ensure_session_state(retrieve_all_threads):
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = generate_thread_id()

    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = retrieve_all_threads()

    if "ingested_docs" not in st.session_state:
        st.session_state["ingested_docs"] = {}

    add_thread(st.session_state["thread_id"])

    thread_key = str(st.session_state["thread_id"])
    thread_docs = st.session_state["ingested_docs"].setdefault(thread_key, {})
    threads = st.session_state["chat_threads"][::-1]

    return thread_key, thread_docs, threads
