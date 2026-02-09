# MEV / Sandwich / Arbitrage detection (high-signal heuristics)
# No false positives by default — conservative rules

from typing import Optional

# Known MEV relays / bots (partial, curated)
MEV_BOTS = {
    "0x0000000000000000000000000000000000000000": "Generic MEV",
}

# Common DEX routers to watch for sandwich patterns
DEX_ROUTERS = {
    "0x7a250d5630b4cf539739df2c5dacab4c659f2488d",  # Uniswap V2
    "0xe592427a0aece92de3edee1f18e0157c05861564",  # Uniswap V3
}


def detect_mev(tx: dict, prev_tx: Optional[dict], next_tx: Optional[dict]) -> str | None:
    """
    Detect MEV patterns using adjacency heuristics:
    - Sandwich: same actor before & after a victim tx on same DEX
    - Arbitrage: multiple DEX interactions in one tx
    """

    to_addr = (tx.get("to") or "").lower()
    from_addr = (tx.get("from") or "").lower()

    # --- Arbitrage: multiple swaps in one tx (router interaction)
    if to_addr in DEX_ROUTERS and tx.get("input", "0x") != "0x":
        if "swap" in tx.get("input", "").lower():
            return "⚡ Arbitrage Activity Detected"

    # --- Sandwich detection (needs neighbors)
    if prev_tx and next_tx:
        p_from = (prev_tx.get("from") or "").lower()
        n_from = (next_tx.get("from") or "").lower()

        if (
            p_from == n_from
            and to_addr in DEX_ROUTERS
            and (prev_tx.get("to") or "").lower() in DEX_ROUTERS
            and (next_tx.get("to") or "").lower() in DEX_ROUTERS
        ):
            return "🥪 MEV Sandwich Attack Pattern"

    # --- Known MEV bot
    if from_addr in MEV_BOTS:
        return f"🤖 MEV Bot Activity ({MEV_BOTS[from_addr]})"

    return None
