# FILE: bot/routers/my_plan.py
# LOCATION: bot/routers/my_plan.py
# DROP-IN REPLACEMENT

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from services.user_tiers import get_tier
from services.typing import typing
from services.streaks import touch, get_streak
from bot.keyboards.main_menu import get_main_menu

router = Router()


def plan_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅ Back to Menu")],
        ],
        resize_keyboard=True,
    )


PLAN_DESCRIPTIONS = {
    "free": [
        "• Delayed alerts",
        "• No smart money labels",
        "• No exchange flow intel",
        "• No behavior analysis",
    ],
    "pro": [
        "• Faster alerts",
        "• Exchange deposit / withdrawal labels",
        "• Wallet labeling",
        "• Limited wallets",
        "• Limited chains",
    ],
    "elite": [
        "• Near-real-time alerts",
        "• Smart money detection",
        "• Advanced wallet labels",
        "• Higher wallet limits",
        "• More chains",
    ],
    "super_elite": [
        "• Instant alerts",
        "• Full smart money detection",
        "• Behavior analysis",
        "• Capital flow intelligence",
        "• Unlimited wallets",
        "• All chains",
        "• No rate limits",
    ],
}

UPGRADE_NUDGE = {
    "free": "🔓 Upgrade to unlock real-time alerts and intelligence.",
    "pro": "⚡ Upgrade to Elite for faster alerts and smart money detection.",
    "elite": "👑 Upgrade to Super Elite for instant alerts and full flow intel.",
}


@router.message(F.text == "📊 My Plan")
async def my_plan(message: Message):
    await typing(message.bot, message.chat.id)

    user_id = message.from_user.id

    await touch(user_id)
    streak = await get_streak(user_id)

    tier = await get_tier(user_id)
    perks = PLAN_DESCRIPTIONS.get(tier, PLAN_DESCRIPTIONS["free"])

    text = [
        "📊 **My Plan**",
        "",
        f"Current tier: **{tier.replace('_', ' ').title()}**",
        f"🔥 Activity streak: **{streak} day{'s' if streak != 1 else ''}**",
        "",
        "What you get:",
    ]

    for line in perks:
        text.append(line)

    if tier in UPGRADE_NUDGE:
        text.extend(["", UPGRADE_NUDGE[tier]])

    await message.answer(
        "\n".join(text),
        reply_markup=plan_keyboard(),
        parse_mode="Markdown",
    )


@router.message(F.text == "⬅ Back to Menu")
async def back_to_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "⬇️ Main Menu",
        reply_markup=get_main_menu(),
    )
