# High-signal exchange wallet clusters

EXCHANGE_WALLETS = {
    # BINANCE
    "0x28c6c06298d514db089934071355e5743bf21d60": "Binance",
    "0x21a31ee1afc51d94c2efccaa2092ad1028285549": "Binance",
    "0xdfd5293d8e347dfe59e90efd55b2956a1343963d": "Binance",

    # COINBASE
    "0x71660c4005ba85c37ccec55d0c4493e66fe775d3": "Coinbase",
    "0x503828976d22510aad0201ac7ec88293211d23da": "Coinbase",

    # KRAKEN
    "0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0": "Kraken",

    # OKX
    "0x8894e0a0c962cb723c1976a4421c95949be2d4e3": "OKX",
}


def label_exchange_flow(from_addr: str, to_addr: str) -> str | None:
    from_addr = from_addr.lower()
    to_addr = to_addr.lower()

    if to_addr in EXCHANGE_WALLETS:
        return f"→ {EXCHANGE_WALLETS[to_addr]} deposit"

    if from_addr in EXCHANGE_WALLETS:
        return f"← {EXCHANGE_WALLETS[from_addr]} withdrawal"

    return None
