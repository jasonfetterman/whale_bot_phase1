from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from services.user_tiers import get_tier
from services.typing import typing
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
    ],
    "elite": [
        "• Near-real-time alerts",
        "• Smart money detection",
        "• Advanced wallet labels",
    ],
    "super_elite": [
        "• Instant alerts",
        "• Full smart money detection",
        "• Behavior analysis",
        "• Capital flow intelligence",
        "• No rate limits",
    ],
}


@router.message(F.text == "📊 My Plan")
async def my_plan(message: Message):
    await typing(message.bot, message.chat.id)

    tier = await get_tier(message.from_user.id)
    perks = PLAN_DESCRIPTIONS.get(tier, [])

    text = [
        "📊 **My Plan**",
        "",
        f"Current tier: **{tier.replace('_', ' ').title()}**",
        "",
        "What you get:",
    ]

    for line in perks:
        text.append(line)

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
