import asyncio
from aiogram.types import Message

async def animated_reply(
    message: Message,
    text: str,
    reply_markup=None,
    delay: float = 0.5,
):
    await message.bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(delay)
    await message.answer(text, reply_markup=reply_markup)
