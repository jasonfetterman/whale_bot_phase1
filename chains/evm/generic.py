async def classify_generic(tx: dict, usd_value: float, chain: str, threshold: float):
    if usd_value >= threshold:
        return f"🐋 {chain.upper()} whale confirmed: ${usd_value:,.0f} | {tx.get('hash')}"
    return None