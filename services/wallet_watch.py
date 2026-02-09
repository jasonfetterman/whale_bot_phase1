from db.engine import get_db


async def get_tracked_wallets() -> dict[str, list[int]]:
    """
    Returns:
    {
        "0xabc...": [chat_id1, chat_id2],
        ...
    }
    """
    db = await get_db()
    cursor = await db.execute(
        "SELECT chat_id, address FROM wallets"
    )
    rows = await cursor.fetchall()

    mapping: dict[str, list[int]] = {}
    for r in rows:
        addr = r["address"].lower()
        mapping.setdefault(addr, []).append(r["chat_id"])

    return mapping
