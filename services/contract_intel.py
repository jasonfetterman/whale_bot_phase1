# High-signal smart-contract interaction detection
# DEX / Bridge / Protocol level awareness

DEX_CONTRACTS = {
    # Uniswap
    "0x7a250d5630b4cf539739df2c5dacab4c659f2488d": "Uniswap V2 Router",
    "0xe592427a0aece92de3edee1f18e0157c05861564": "Uniswap V3 Router",

    # Sushi
    "0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f": "SushiSwap Router",

    # Curve
    "0xdef1c0ded9bec7f1a1670819833240f027b25eff": "Curve Router",
}

BRIDGE_CONTRACTS = {
    # Arbitrum
    "0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f": "Arbitrum Bridge",

    # Optimism
    "0x99c9fc46f92e8a1c0dec1b1747d010903e884be1": "Optimism Bridge",

    # Polygon
    "0xa0c68c638235ee32657e8f720a23ce9c1bfc77c7": "Polygon Bridge",
}

PROTOCOL_CONTRACTS = {
    # Lido
    "0xae7ab96520de3a18e5e111b5eaab095312d7fe84": "Lido Staking",

    # Aave
    "0x7beA39867e4169DBe237d55C8242a8f2fcDcc387".lower(): "Aave Lending",

    # Maker
    "0x9759a6ac90977b93b58547b4a71c78317f391a28": "MakerDAO",
}


def detect_contract_intel(to_addr: str) -> str | None:
    if not to_addr:
        return None

    addr = to_addr.lower()

    if addr in DEX_CONTRACTS:
        return f"🔁 DEX Interaction: {DEX_CONTRACTS[addr]}"

    if addr in BRIDGE_CONTRACTS:
        return f"🌉 Bridge Interaction: {BRIDGE_CONTRACTS[addr]}"

    if addr in PROTOCOL_CONTRACTS:
        return f"🏦 Protocol Interaction: {PROTOCOL_CONTRACTS[addr]}"

    return None
