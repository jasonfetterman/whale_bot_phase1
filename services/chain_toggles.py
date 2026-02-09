from db.engine import get_db

# defaults: enabled unless explicitly disabled
async def is_chain_enabled(user_id: int, chain: str) -> bool:
    db = await get_db()
    cur = await db.execute(
        "SELECT enabled FROM chain_toggles WHERE user_id = ? AND chain = ?",
        (user_id, chain),
    )
    row = await cur.fetchone()
    if row is None:
        return True
    return bool(row["enabled"])


async def set_chain_enabled(user_id: int, chain: str, enabled: bool):
    db = await get_db()
    await db.execute(
        """
        INSERT INTO chain_toggles (user_id, chain, enabled)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, chain)
        DO UPDATE SET enabled = excluded.enabled
        """,
        (user_id, chain, int(enabled)),
    )
    await db.commit()
