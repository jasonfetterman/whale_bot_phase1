from db.engine import get_db


async def upsert_user(chat_id: int, tier: str, status: str = "active"):
    db = await get_db()
    await db.execute(
        """
        INSERT INTO users (chat_id, tier, status)
        VALUES (?, ?, ?)
        ON CONFLICT(chat_id) DO UPDATE SET
            tier = excluded.tier,
            status = excluded.status
        """,
        (chat_id, tier, status),
    )
    await db.commit()


async def get_user_tier(chat_id: int) -> str | None:
    db = await get_db()
    cursor = await db.execute(
        "SELECT tier FROM users WHERE chat_id = ?", (chat_id,)
    )
    row = await cursor.fetchone()
    return row["tier"] if row else None
