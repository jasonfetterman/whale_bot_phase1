from aiogram import Router, F
from aiogram.types import Message
import json
import os

from services.user_tiers import get_tier

router = Router()

LINK_FILE = "telegram_links.json"


def load_links():
    if not os.path.exists(LINK_FILE):
        return {}
    with open(LINK_FILE, "r") as f:
        return json.load(f)


def save_links(data):
    with open(LINK_FILE, "w") as f:
        json.dump(data, f, indent=2)


@router.message(F.text.len() == 8)
async def link_account(message: Message):
    code = message.text.lower()
    telegram_id = str(message.from_user.id)

    # READ tier but DO NOT MODIFY IT
    tier = await get_tier(message.from_user.id)

    links = load_links()

    links[telegram_id] = {
        "link_code": code,
        "telegram_username": message.from_user.username,
        "tier_at_link_time": tier,  # audit only, not authoritative
    }

    save_links(links)

    await message.answer(
        "✅ Telegram account linked successfully.\n\n"
        "You can now return to the web app."
    )
