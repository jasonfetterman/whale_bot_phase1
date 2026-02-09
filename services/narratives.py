def build_narrative(
    *,
    chain: str,
    amount: float,
    symbol: str,
    from_addr: str | None,
    to_addr: str | None,
) -> tuple[str, str, str]:
    """
    Returns:
        direction (IN / OUT)
        counterparty address (or 'unknown')
        narrative sentence
    """

    # Direction logic
    direction = "OUT" if from_addr else "IN"
    counterparty = to_addr if direction == "OUT" else from_addr
    counterparty = counterparty or "unknown"

    # Base narratives by chain
    base_narratives = {
        "eth": (
            "Large ETH movement detected. Transfers of this size often precede "
            "liquidity shifts, exchange activity, or internal fund movements."
        ),
        "bsc": (
            "Large BNB movement detected. Transfers of this size often indicate "
            "exchange flows, liquidity adjustments, or treasury operations."
        ),
        "polygon": (
            "Large MATIC transfer detected. High-value Polygon movements often "
            "relate to bridge activity or exchange liquidity."
        ),
        "arbitrum": (
            "Large ETH transfer on Arbitrum detected. Movements of this size on "
            "Layer 2 frequently signal bridge flows or major trader positioning."
        ),
        "base": (
            "Large ETH transfer on Base detected. High-value Base movements often "
            "reflect exchange routing or bridge-related activity."
        ),
    }

    narrative = base_narratives.get(
        chain,
        "Large on-chain transfer detected."
    )

    return direction, counterparty, narrative
