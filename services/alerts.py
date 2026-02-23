# FILE: services/alerts.py
# LOCATION: services/alerts.py
# DROP-IN REPLACEMENT

import time
import asyncio
from aiogram import Bot

from services.user_tiers import get_tier
from services.mute_windows import is_muted
from services.metrics import inc_alerts
from db.engine import get_db

# ---- tier latency (seconds) ----
TIER_DELAY = {
    "free": 120,
    "pro": 20,
    "elite": 5,
    "super_elite": 0,
}

# ---- tier rate caps (alerts per hour) ----
TIER_RATE_CAP = {
    "free": 0,
    "pro": 30,
    "elite": 120,
    "super_elite": float("inf"),
}

# ---- in-memory rate window ----
_SENT_LOG: dict[int, list[float]] = {}
_WINDOW = 60 * 60  # 1 hour

# ---- dedupe ----
_TTL = 60 * 60


async def _seen(tx_hash: str) -> bool:
    db = await get_db()
    cur = await db.execute(
        "SELECT 1 FROM alerts_seen WHERE alert_key = ?",
        (tx_hash,),
    )
    return await cur.fetchone() is not None


async def _mark_seen(tx_hash: str):
    db = await get_db()
    await db.execute(
        """
        INSERT OR IGNORE INTO alerts_seen (alert_key, seen_at)
        VALUES (?, ?)
        """,
        (tx_hash, int(time.time())),
    )
    await db.commit()


async def _cleanup_seen():
    cutoff = int(time.time()) - _TTL
    db = await get_db()
    await db.execute(
        "DELETE FROM alerts_seen WHERE seen_at < ?",
        (cutoff,),
    )
    await db.commit()


def _rate_allowed(chat_id: int, tier: str) -> bool:
    limit = TIER_RATE_CAP.get(tier, 0)
    if limit == float("inf"):
        return True

    now = time.time()
    bucket = _SENT_LOG.setdefault(chat_id, [])
    bucket[:] = [t for t in bucket if now - t < _WINDOW]

    if len(bucket) >= limit:
        return False

    bucket.append(now)
    return True


async def emit(bot: Bot, chat_id: int, text: str | None):
    if not text:
        return

    await _cleanup_seen()

    tx_hash = None
    for line in text.splitlines():
        if line.startswith("TX:"):
            tx_hash = line.replace("TX:", "").strip()
            break

    if tx_hash and await _seen(tx_hash):
        return

    tier = await get_tier(chat_id)
    if tier == "free":
        return

    if is_muted(chat_id):
        return

    if not _rate_allowed(chat_id, tier):
        return

    delay = TIER_DELAY.get(tier, 0)
    if delay:
        await asyncio.sleep(delay)

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=None,
    )

    inc_alerts()  # 📊 metric — only after send

    if tx_hash:
        await _mark_seen(tx_hash)
