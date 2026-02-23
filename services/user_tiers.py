from db.engine import get_db


async def get_tier(chat_id: int) -> str:
    db = await get_db()
    cursor = await db.execute(
        "SELECT tier FROM users WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cursor.fetchone()
    await cursor.close()

    if row is None:
        return "free"

    return row["tier"]


async def set_tier(chat_id: int, tier: str):
    db = await get_db()
    await db.execute(
        """
        INSERT INTO users (chat_id, tier, status)
        VALUES (?, ?, 'active')
        ON CONFLICT(chat_id) DO UPDATE SET tier = excluded.tier
        """,
        (chat_id, tier),
    )
    await db.commit()
