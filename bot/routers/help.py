from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from bot.keyboards.main_menu import get_main_menu
from services.typing import typing

router = Router()


def help_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📘 How It Works")],
            [KeyboardButton(text="💎 Plans & Tiers")],
            [KeyboardButton(text="🧪 Troubleshooting")],
            [KeyboardButton(text="⬅ Back to Menu")],
        ],
        resize_keyboard=True,
    )


# 🔒 FORCE ENTRY — COMMAND ALWAYS WINS
@router.message(Command("help"))
async def help_command(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "❓ Help Center\n\nChoose a topic below 👇",
        reply_markup=help_keyboard(),
    )


# 🔒 FORCE ENTRY — EXACT TEXT
@router.message(lambda m: m.text == "❓ Help")
async def help_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "❓ Help Center\n\nChoose a topic below 👇",
        reply_markup=help_keyboard(),
    )


@router.message(lambda m: m.text == "📘 How It Works")
async def how_it_works(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "📘 How Whaler X Works\n\n"
        "• Monitors live blockchain activity\n"
        "• Detects whale transactions\n"
        "• Applies plan-based intelligence\n"
        "• Delivers alerts to Telegram\n",
        reply_markup=help_keyboard(),
    )


@router.message(lambda m: m.text == "💎 Plans & Tiers")
async def plans_and_tiers(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "💎 Plans & Tiers\n\n"
        "🆓 Free\n"
        "• Heavy delay\n"
        "• No intelligence\n\n"
        "🚀 Pro\n"
        "• Faster alerts\n"
        "• Exchange labels\n\n"
        "🔥 Elite\n"
        "• Near-real-time\n"
        "• Smart money\n\n"
        "👑 Super Elite\n"
        "• Instant alerts\n"
        "• Behavior + flow intel\n",
        reply_markup=help_keyboard(),
    )


@router.message(lambda m: m.text == "🧪 Troubleshooting")
async def troubleshooting(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "🧪 Troubleshooting\n\n"
        "• No alerts = normal\n"
        "• Threshold may be high\n"
        "• Restart after changes\n",
        reply_markup=help_keyboard(),
    )


@router.message(lambda m: m.text == "⬅ Back to Menu")
async def back_to_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "⬇️ Main Menu",
        reply_markup=get_main_menu(),
    )
