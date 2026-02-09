from services.user_tiers import get_tier

# chains user is allowed to receive alerts from
CHAIN_ACCESS = {
    "free": {"eth"},
    "pro": {"eth", "bsc"},
    "elite": {"eth", "bsc", "polygon", "arbitrum", "base"},
    "super_elite": {"eth", "bsc", "polygon", "arbitrum", "base"},
}


async def can_access_chain(user_id: int, chain: str) -> bool:
    tier = await get_tier(user_id)
    return chain in CHAIN_ACCESS.get(tier, set())
