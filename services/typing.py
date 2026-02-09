import asyncio
from aiogram import Bot


async def typing(bot: Bot, chat_id: int):
    """
    Fire-and-forget typing indicator.
    Never blocks handlers or delays UI.
    """
    async def _send():
        try:
            await bot.send_chat_action(chat_id, "typing")
        except Exception:
            pass

    # 🔥 critical: do NOT await
    asyncio.create_task(_send())
