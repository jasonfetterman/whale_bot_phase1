import sys
import asyncio
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import db.engine  # noqa: F401

from aiogram import Bot, Dispatcher
from config.settings import settings

from bot.routers.start import router as start_router
from bot.routers.help import router as help_router
from bot.routers.whale_alerts import router as whale_alerts_router
from bot.routers.settings import router as settings_router
from bot.routers.my_plan import router as my_plan_router
from bot.routers.upgrade import router as upgrade_router
from bot.routers.admin import router as admin_router
from bot.routers.restart import router as restart_router
from bot.routers.wallets import router as wallets_router
from bot.routers.link_account import router as link_router

from services.alchemy_ws import AlchemyWS
from services.eth_confirmed import handle_block as handle_eth
from services.user_tiers import set_tier
from db.engine import init_db


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(whale_alerts_router)
    dp.include_router(settings_router)
    dp.include_router(my_plan_router)
    dp.include_router(upgrade_router)
    dp.include_router(admin_router)
    dp.include_router(restart_router)
    dp.include_router(wallets_router)
    dp.include_router(link_router)

    await init_db()
    await set_tier(settings.OWNER_CHAT_ID, "super_elite")

    async def on_eth_block(head):
        await handle_eth(bot, head)

    eth_ws = AlchemyWS(
        f"wss://eth-mainnet.g.alchemy.com/v2/{settings.ALCHEMY_KEY}"
    )
    asyncio.create_task(eth_ws.run(on_eth_block))

    # ---- POLLING MODE ----
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
