from services.pricing import get_eth_usd

async def classify_tx(tx: dict, threshold: float) -> str | None:
    value = int(tx.get("value", "0"), 16)
    usd = (value / 1e18) * await get_eth_usd()
    if usd >= threshold:
        return f"🐋 ETH whale confirmed: ${usd:,.0f} | {tx.get('hash')}"
    return None