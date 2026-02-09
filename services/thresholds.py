from db.engine import get_db
from config.settings import settings


# =========================
# READ THRESHOLD (PER USER)
# =========================
async def get_for_user(
    chain: str,
    user_id: int,
    default: float,
) -> float:
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT value
        FROM thresholds
        WHERE chain = ? AND user_id = ?
        """,
        (chain, user_id),
    )
    row = await cursor.fetchone()

    if row:
        return float(row["value"])

    return float(default)


# =========================
# READ THRESHOLD (OWNER)
# =========================
async def get(chain: str, default: float) -> float:
    return await get_for_user(
        chain=chain,
        user_id=settings.OWNER_CHAT_ID,
        default=default,
    )


# =========================
# WRITE THRESHOLD (PER USER)
# =========================
async def set_for_user(
    chain: str,
    user_id: int,
    value: float,
):
    db = await get_db()

    await db.execute(
        """
        INSERT INTO thresholds (chain, user_id, value)
        VALUES (?, ?, ?)
        ON CONFLICT(chain, user_id)
        DO UPDATE SET value = excluded.value
        """,
        (chain, user_id, float(value)),
    )
    await db.commit()


# =========================
# OWNER COMPATIBILITY
# =========================
async def set(chain: str, value: float):
    await set_for_user(
        chain=chain,
        user_id=settings.OWNER_CHAT_ID,
        value=value,
    )
