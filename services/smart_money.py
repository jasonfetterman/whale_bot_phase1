# High-signal smart money clusters
# Funds, VCs, known whale operators

SMART_MONEY_WALLETS = {
    # FUNDS / VCs
    "0x742d35cc6634c0532925a3b844bc454e4438f44e": "Jump Trading",
    "0x564286362092d8e7936f0549571a803b203aaced": "Paradigm",
    "0x9d89bdf4d0c5f7c52b8c9f0ed7fbe2f1a4a9a7c2": "Wintermute",
    "0x4fabb145d64652a948d72533023f6e7a623c7c53": "Alameda",

    # WHALES
    "0x00000000219ab540356cbb839cbe05303d7705fa": "Ethereum Foundation",
}


def smart_money_label(from_addr: str, to_addr: str) -> str | None:
    from_addr = from_addr.lower()
    to_addr = to_addr.lower()

    if from_addr in SMART_MONEY_WALLETS:
        return f"🐋 Smart Money OUT — {SMART_MONEY_WALLETS[from_addr]}"

    if to_addr in SMART_MONEY_WALLETS:
        return f"🐋 Smart Money IN — {SMART_MONEY_WALLETS[to_addr]}"

    return None
