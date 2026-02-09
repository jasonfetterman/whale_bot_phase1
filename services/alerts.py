import time
import asyncio
from aiogram import Bot

from services.user_tiers import get_tier
from services.mute_windows import is_muted
from db.engine import get_db

# ---- tier latency (seconds) ----
TIER_DELAY = {
    "free": 120,
    "pro": 20,
    "elite": 5,
    "super_elite": 0,
}

# ---- intelligence stripping ----
INTEL_FILTERS = {
    "free": {"SMART", "BEHAVIOR", "FLOW"},
    "pro": {"BEHAVIOR", "FLOW"},
    "elite": {"FLOW"},
    "super_elite": set(),
}

# ---- rate limiting ----
_LAST_SENT: dict[int, float] = {}
_MIN_INTERVAL = 3.0
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


async def _cleanup():
    cutoff = int(time.time()) - _TTL
    db = await get_db()
    await db.execute(
        "DELETE FROM alerts_seen WHERE seen_at < ?",
        (cutoff,),
    )
    await db.commit()


def _filter_intel(text: str, tier: str) -> str:
    blocked = INTEL_FILTERS.get(tier, set())
    if not blocked:
        return text

    out = []
    for line in text.splitlines():
        if any(b in line for b in blocked):
            continue
        out.append(line)

    return "\n".join(out)


async def emit(bot: Bot, chat_id: int, text: str | None):
    if not text:
        return

    await _cleanup()
    now = time.time()

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

    delay = TIER_DELAY.get(tier, 0)
    if delay:
        await asyncio.sleep(delay)

    last = _LAST_SENT.get(chat_id, 0)
    if now - last < _MIN_INTERVAL:
        return

    msg = _filter_intel(text, tier)

    await bot.send_message(
        chat_id=chat_id,
        text=msg,
        parse_mode=None,
    )

    _LAST_SENT[chat_id] = time.time()

    if tx_hash:
        await _mark_seen(tx_hash)
