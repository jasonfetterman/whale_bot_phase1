# FILE: services/referral_perks.py
# LOCATION: services/referral_perks.py
# DROP-IN REPLACEMENT

from db.engine import get_db

# CONFIG
CREDITS_PER_DAY = 5  # 5 credits = 1 free day
AUTO_THRESHOLDS = [5, 10, 25, 50, 100]  # credits milestones


async def _ensure_tables():
    db = await get_db()

    # stores granted free days
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS referral_perks (
            chat_id INTEGER PRIMARY KEY,
            free_days INTEGER DEFAULT 0
        )
        """
    )

    # tracks which thresholds were already granted
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS referral_grants (
            chat_id INTEGER,
            threshold INTEGER,
            PRIMARY KEY (chat_id, threshold)
        )
        """
    )

    await db.commit()


async def grant_free_days(chat_id: int, days: int):
    await _ensure_tables()
    db = await get_db()

    await db.execute(
        """
        INSERT INTO referral_perks (chat_id, free_days)
        VALUES (?, ?)
        ON CONFLICT(chat_id)
        DO UPDATE SET free_days = free_days + ?
        """,
        (chat_id, days, days),
    )

    await db.commit()


async def get_free_days(chat_id: int) -> int:
    await _ensure_tables()
    db = await get_db()

    cur = await db.execute(
        "SELECT free_days FROM referral_perks WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cur.fetchone()
    return row["free_days"] if row else 0


async def maybe_auto_grant(chat_id: int, total_credits: int):
    """
    Auto-grant free days when credit thresholds are crossed.
    Each threshold is granted only once.
    """
    await _ensure_tables()
    db = await get_db()

    for threshold in AUTO_THRESHOLDS:
        if total_credits < threshold:
            continue

        cur = await db.execute(
            """
            SELECT 1 FROM referral_grants
            WHERE chat_id = ? AND threshold = ?
            """,
            (chat_id, threshold),
        )
        if await cur.fetchone():
            continue  # already granted

        days = threshold // CREDITS_PER_DAY
        await grant_free_days(chat_id, days)

        await db.execute(
            """
            INSERT INTO referral_grants (chat_id, threshold)
            VALUES (?, ?)
            """,
            (chat_id, threshold),
        )

    await db.commit()
