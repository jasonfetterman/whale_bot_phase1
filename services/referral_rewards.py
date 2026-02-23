# FILE: services/referral_rewards.py
# LOCATION: services/referral_rewards.py
# DROP-IN REPLACEMENT

from db.engine import get_db
from services.referral_perks import maybe_auto_grant

# reward units = abstract credits
REFERRAL_REWARD_CREDITS = 10


async def _ensure_table():
    db = await get_db()
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS referral_rewards (
            chat_id INTEGER PRIMARY KEY,
            credits INTEGER DEFAULT 0,
            referrals INTEGER DEFAULT 0
        )
        """
    )
    await db.commit()


async def credit_referrer(chat_id: int):
    await _ensure_table()
    db = await get_db()

    # increment credits + referrals
    await db.execute(
        """
        INSERT INTO referral_rewards (chat_id, credits, referrals)
        VALUES (?, ?, 1)
        ON CONFLICT(chat_id)
        DO UPDATE SET
            credits = credits + ?,
            referrals = referrals + 1
        """,
        (chat_id, REFERRAL_REWARD_CREDITS, REFERRAL_REWARD_CREDITS),
    )
    await db.commit()

    # fetch updated total credits
    cur = await db.execute(
        "SELECT credits FROM referral_rewards WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cur.fetchone()
    total_credits = row["credits"] if row else 0

    # 🔥 auto-grant perks if thresholds crossed
    await maybe_auto_grant(chat_id, total_credits)


async def get_rewards(chat_id: int) -> dict:
    await _ensure_table()
    db = await get_db()

    cur = await db.execute(
        "SELECT credits, referrals FROM referral_rewards WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cur.fetchone()

    if not row:
        return {"credits": 0, "referrals": 0}

    return {
        "credits": row["credits"],
        "referrals": row["referrals"],
    }
