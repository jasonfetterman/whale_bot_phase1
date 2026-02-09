# SYNC ONLY — MUST RETURN STRING OR NONE

EXCHANGE_WALLETS = {
    "0x28c6c06298d514db089934071355e5743bf21d60": "Binance",
    "0x21a31ee1afc51d94c2efccaa2092ad1028285549": "Binance",
    "0x71660c4005ba85c37ccec55d0c4493e66fe775d3": "Coinbase",
    "0x503828976d22510aad0201ac7ec88293211d23da": "Coinbase",
    "0x742d35cc6634c0532925a3b844bc454e4438f44e": "Bitfinex",
}


def label_tx(tx: dict) -> str | None:
    to_addr = (tx.get("to") or "").lower()
    from_addr = (tx.get("from") or "").lower()

    if to_addr in EXCHANGE_WALLETS:
        return f"→ {EXCHANGE_WALLETS[to_addr]} (deposit)"

    if from_addr in EXCHANGE_WALLETS:
        return f"← {EXCHANGE_WALLETS[from_addr]} (withdrawal)"

    return None
