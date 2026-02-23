# FILE: services/referrals.py
# LOCATION: services/referrals.py
# DROP-IN REPLACEMENT

import hashlib
import time
from db.engine import get_db
from services.referral_rewards import credit_referrer

# ---- FRAUD LIMITS ----
MAX_REFERRALS_PER_DAY = 5
COOLDOWN_SECONDS = 60 * 10  # 10 minutes


async def _ensure_tables():
    db = await get_db()

    # main referral mapping
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS referrals (
            chat_id INTEGER PRIMARY KEY,
            code TEXT UNIQUE,
            referred_by INTEGER
        )
        """
    )

    # referral activity log (for fraud limits)
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS referral_activity (
            referrer_id INTEGER,
            referred_id INTEGER,
            ts INTEGER
        )
        """
    )

    await db.commit()


def _make_code(chat_id: int) -> str:
    return hashlib.sha256(str(chat_id).encode()).hexdigest()[:8]


async def get_or_create_code(chat_id: int) -> str:
    await _ensure_tables()
    db = await get_db()

    cur = await db.execute(
        "SELECT code FROM referrals WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cur.fetchone()
    if row:
        return row["code"]

    code = _make_code(chat_id)
    await db.execute(
        "INSERT INTO referrals (chat_id, code) VALUES (?, ?)",
        (chat_id, code),
    )
    await db.commit()
    return code


async def _passes_limits(referrer_id: int) -> bool:
    """
    Enforce:
    - cooldown between referrals
    - max referrals per 24h
    """
    now = int(time.time())
    day_ago = now - 86400

    db = await get_db()
    cur = await db.execute(
        """
        SELECT ts FROM referral_activity
        WHERE referrer_id = ?
        ORDER BY ts DESC
        """,
        (referrer_id,),
    )
    rows = await cur.fetchall()

    if rows:
        # cooldown check
        if now - rows[0]["ts"] < COOLDOWN_SECONDS:
            return False

        # daily cap
        recent = [r for r in rows if r["ts"] >= day_ago]
        if len(recent) >= MAX_REFERRALS_PER_DAY:
            return False

    return True


async def apply_referral(chat_id: int, code: str):
    """
    Apply referral only once.
    Silent fail on:
    - invalid code
    - self-referral
    - duplicate referral
    - fraud limits
    """
    await _ensure_tables()
    db = await get_db()

    cur = await db.execute(
        "SELECT chat_id FROM referrals WHERE code = ?",
        (code,),
    )
    row = await cur.fetchone()
    if not row:
        return

    referrer_id = row["chat_id"]
    if referrer_id == chat_id:
        return

    # already referred?
    cur = await db.execute(
        "SELECT referred_by FROM referrals WHERE chat_id = ?",
        (chat_id,),
    )
    existing = await cur.fetchone()
    if existing and existing["referred_by"] is not None:
        return

    # fraud limits
    if not await _passes_limits(referrer_id):
        return

    # apply referral
    await db.execute(
        """
        INSERT INTO referrals (chat_id, referred_by)
        VALUES (?, ?)
        ON CONFLICT(chat_id)
        DO UPDATE SET referred_by = excluded.referred_by
        """,
        (chat_id, referrer_id),
    )

    # log activity
    await db.execute(
        """
        INSERT INTO referral_activity (referrer_id, referred_id, ts)
        VALUES (?, ?, ?)
        """,
        (referrer_id, chat_id, int(time.time())),
    )

    await credit_referrer(referrer_id)
    await db.commit()
