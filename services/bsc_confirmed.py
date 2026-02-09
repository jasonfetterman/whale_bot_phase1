import aiohttp
from aiogram import Bot

from config.settings import settings
from services.alerts import emit
from services.thresholds import get_for_user
from services.narratives import build_narrative
from services.entities import resolve_entity
from services.importance import score_importance

RPC_URL = "https://bsc-dataseed.binance.org"


async def handle_bsc_block(bot: Bot, head: dict):
    block_number = head.get("number")
    if not block_number:
        return

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBlockByNumber",
        "params": [block_number, True],
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(RPC_URL, json=payload, timeout=10) as r:
                if r.status != 200:
                    return
                data = await r.json()
    except Exception:
        return

    block = data.get("result")
    if not isinstance(block, dict):
        return

    threshold = await get_for_user(
        chain="bsc",
        user_id=settings.OWNER_CHAT_ID,
        default=settings.BSC_WHALE_THRESHOLD,
    )

    txs = block.get("transactions")
    if not isinstance(txs, list):
        return

    for tx in txs:
        try:
            value_hex = tx.get("value")
            from_addr = tx.get("from")
            to_addr = tx.get("to")
            tx_hash = tx.get("hash")

            if not value_hex or not from_addr or not tx_hash:
                continue

            value_bnb = int(value_hex, 16) / 1e18
            if value_bnb < threshold:
                continue

            direction, counterparty, narrative = build_narrative(
                chain="bsc",
                amount=value_bnb,
                symbol="BNB",
                from_addr=from_addr,
                to_addr=to_addr,
            )

            entity = resolve_entity(counterparty)
            counterparty_display = entity or counterparty

            importance = score_importance(value_bnb, threshold)

            await emit(
                bot=bot,
                chat_id=settings.OWNER_CHAT_ID,
                wallet=from_addr,
                chain="bsc",
                text=(
                    "🐋 BSC Whale Alert\n"
                    f"Amount: {value_bnb:.2f} BNB\n"
                    f"Importance: {importance}\n"
                    f"Direction: {direction}\n"
                    f"Counterparty: {counterparty_display}\n"
                    f"{narrative}\n"
                    f"TX: {tx_hash}"
                ),
            )

        except Exception:
            continue


# compatibility alias
handle_block = handle_bsc_block
