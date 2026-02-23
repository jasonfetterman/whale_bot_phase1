# FILE: services/streaks.py
# LOCATION: services/streaks.py
# NEW FILE — DROP-IN

import time
from db.engine import get_db

_DAY = 60 * 60 * 24


async def _ensure_table():
    db = await get_db()
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS user_streaks (
            chat_id INTEGER PRIMARY KEY,
            last_seen INTEGER,
            streak INTEGER
        )
        """
    )
    await db.commit()


async def touch(chat_id: int):
    """
    Call this on any meaningful user interaction.
    """
    await _ensure_table()
    now = int(time.time())

    db = await get_db()
    cur = await db.execute(
        "SELECT last_seen, streak FROM user_streaks WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cur.fetchone()

    if not row:
        await db.execute(
            "INSERT INTO user_streaks (chat_id, last_seen, streak) VALUES (?, ?, ?)",
            (chat_id, now, 1),
        )
        await db.commit()
        return

    last_seen, streak = row
    delta = now - last_seen

    if delta >= _DAY * 2:
        streak = 1
    elif delta >= _DAY:
        streak += 1

    await db.execute(
        "UPDATE user_streaks SET last_seen = ?, streak = ? WHERE chat_id = ?",
        (now, streak, chat_id),
    )
    await db.commit()


async def get_streak(chat_id: int) -> int:
    await _ensure_table()
    db = await get_db()
    cur = await db.execute(
        "SELECT streak FROM user_streaks WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cur.fetchone()
    return row["streak"] if row else 0
