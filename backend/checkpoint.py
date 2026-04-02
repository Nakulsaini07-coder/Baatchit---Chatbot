from __future__ import annotations

import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


async def init_checkpointer(database: str = "chatbot.db"):
    conn = await aiosqlite.connect(database=database)
    return AsyncSqliteSaver(conn)
