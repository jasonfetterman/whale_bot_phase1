import aiohttp
from aiogram import Bot

from config.settings import settings
from services.alerts import emit
from services.thresholds import get_for_user

RPC_URL = f"https://eth-mainnet.g.alchemy.com/v2/{settings.ALCHEMY_KEY}"


async def handle_block(bot: Bot, head: dict):
    block_hash = head.get("hash")
    if not block_hash:
        return

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBlockByHash",
        "params": [block_hash, True],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(RPC_URL, json=payload) as r:
            data = await r.json()

    threshold = await get_for_user(
        chain="eth",
        user_id=settings.OWNER_CHAT_ID,
        default=settings.ETH_WHALE_THRESHOLD,
    )

    txs = data.get("result", {}).get("transactions", [])
    for tx in txs:
        value_eth = int(tx.get("value", "0"), 16) / 1e18
        if value_eth < threshold:
            continue

        await emit(
            bot=bot,
            chat_id=settings.OWNER_CHAT_ID,
            text=(
                "🐋 ETH Whale\n"
                f"Threshold: {threshold} ETH\n"
                f"TX: {tx['hash']}"
            ),
        )
