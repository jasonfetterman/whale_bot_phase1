# FILE: bot/routers/admin.py
# LOCATION: bot/routers/admin.py
# DROP-IN REPLACEMENT

from aiogram import Router, F
from aiogram.types import Message
import json
import time

from config.settings import settings
from services.typing import typing
from services.metrics import get_metrics
from services.user_tiers import get_tier
from services.referral_rewards import get_rewards
from services.referral_perks import grant_free_days
from db.engine import get_db

router = Router()


def _is_owner(message: Message) -> bool:
    return message.from_user.id == settings.OWNER_CHAT_ID


async def _get_referral_leaderboard(limit: int = 5) -> list[dict]:
    db = await get_db()
    cur = await db.execute(
        """
        SELECT chat_id, referrals, credits
        FROM referral_rewards
        ORDER BY referrals DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = await cur.fetchall()
    return [
        {
            "chat_id": r["chat_id"],
            "referrals": r["referrals"],
            "credits": r["credits"],
        }
        for r in rows
    ]


def _pct(part: int, whole: int) -> float:
    if whole <= 0:
        return 0.0
    return round((part / whole) * 100, 2)


@router.message(F.text == "📊 Admin")
async def admin_panel(message: Message):
    user_id = message.from_user.id
    tier = await get_tier(user_id)

    if user_id != settings.OWNER_CHAT_ID and tier != "super_elite":
        return

    await typing(message.bot, message.chat.id)

    metrics = await get_metrics()
    leaderboard = await _get_referral_leaderboard()

    starts = metrics.get("starts", 0)
    wallets = metrics.get("wallet_adds", 0)
    upgrades = metrics.get("upgrade_clicks", 0)

    text = [
        "📊 **Admin Dashboard**",
        "",
        "🔁 **Conversion Funnel**",
        f"▶️ Starts: {starts}",
        f"👛 Wallets added: {wallets} ({_pct(wallets, starts)}%)",
        f"💳 Upgrade clicks: {upgrades} ({_pct(upgrades, wallets)}%)",
        "",
        "📈 **System Metrics**",
        f"👥 Active users: {metrics['users']}",
        f"🚨 Alerts sent: {metrics['alerts']}",
        f"⏱ Avg latency: {metrics['latency']}s",
        f"🔌 WS reconnects: {metrics['reconnects']}",
        "",
        "🧾 Export:",
        "`/export_analytics`",
    ]

    if leaderboard:
        text.append("")
        text.append("🎁 **Top Referrers**")
        for i, r in enumerate(leaderboard, start=1):
            text.append(
                f"{i}. `{r['chat_id']}` — "
                f"{r['referrals']} referrals · {r['credits']} credits"
            )

    await message.answer("\n".join(text), parse_mode="Markdown")


@router.message(F.text.startswith("/export_analytics"))
async def export_analytics(message: Message):
    if not _is_owner(message):
        return

    metrics = await get_metrics()
    payload = {
        "exported_at": int(time.time()),
        "metrics": metrics,
    }

    await message.answer(json.dumps(payload, indent=2))


@router.message(F.text.startswith("/grant_days"))
async def grant_days(message: Message):
    if not _is_owner(message):
        return

    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Usage: /grant_days <telegram_id> <days>")
        return

    try:
        tg_id = int(parts[1])
        days = int(parts[2])
    except ValueError:
        await message.answer("Invalid arguments")
        return

    rewards = await get_rewards(tg_id)
    if rewards["credits"] < days * 5:
        await message.answer("❌ Not enough credits")
        return

    await grant_free_days(tg_id, days)
    await message.answer(f"✅ Granted {days} free day(s) to `{tg_id}`", parse_mode="Markdown")


@router.message(F.text.startswith("/check_tier"))
async def check_tier(message: Message):
    if not _is_owner(message):
        return

    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Usage: /check_tier <telegram_id>")
        return

    try:
        tg_id = int(parts[1])
    except ValueError:
        await message.answer("Invalid telegram_id")
        return

    tier = await get_tier(tg_id)
    await message.answer(f"Telegram ID {tg_id} → tier: {tier}")
