# FILE: bot/routers/whale_alerts.py
# LOCATION: bot/routers/whale_alerts.py
# DROP-IN REPLACEMENT

from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.main_menu import get_main_menu
from services.typing import typing
from services.alerts import emit
from services.user_tiers import get_tier

router = Router()


@router.message(F.text == "🚨 Whale Alerts")
async def whale_alerts_status(message: Message):
    await typing(message.bot, message.chat.id)

    tier = await get_tier(message.from_user.id)

    # FREE — BLOCKED
    if tier == "free":
        await message.answer(
            "🚫 Whale Alerts Locked\n\n"
            "Live whale alerts are available on paid plans.",
            reply_markup=get_main_menu(),
        )
        return

    # PRO / ELITE — LIMITED PREVIEW
    if tier in ("pro", "elite"):
        await message.answer(
            "🐋 Whale Alerts (Limited)\n\n"
            "Upgrade to Super Elite to unlock:\n"
            "• All chains\n"
            "• Lowest thresholds\n"
            "• Priority delivery",
            reply_markup=get_main_menu(),
        )
        return

    # SUPER ELITE — FULL ACCESS
    await emit(
        bot=message.bot,
        chat_id=message.chat.id,
        text=(
            "🐋 Whale Alert\n"
            "Amount: 1,234.56 ETH\n"
            "Direction: OUT\n"
            "Counterparty: 0xabc…def\n"
            "Large on-chain transfer detected.\n"
            "TX: LIVE"
        ),
    )

    await message.answer(
        "🚨 Whale Alerts\n\n"
        "✅ Full access enabled\n"
        "🔓 Tier: Super Elite",
        reply_markup=get_main_menu(),
    )
