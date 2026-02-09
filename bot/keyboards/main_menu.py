from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚨 Whale Alerts")],
            [KeyboardButton(text="👛 Wallets")],
            [KeyboardButton(text="📊 My Plan")],
            [KeyboardButton(text="⚙ Settings")],
            [KeyboardButton(text="🚀 Upgrade")],
            [KeyboardButton(text="❓ Help")],
        ],
        resize_keyboard=True,
    )
