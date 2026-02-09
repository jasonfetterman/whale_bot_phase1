from config.settings import settings
from services.user_tiers import get_tier

# ---- chain access by tier ----
# free: ETH only
# pro: ETH + BSC + Polygon
# elite / super_elite: all chains

TIER_CHAINS = {
    "free": {"eth"},
    "pro": {"eth", "bsc", "polygon"},
    "elite": {"eth", "bsc", "polygon", "arbitrum", "base"},
    "super_elite": {"eth", "bsc", "polygon", "arbitrum", "base"},
}


async def can_receive_alert(user_id: int, chain: str | None = None) -> bool:
    """
    Decide if a user can receive alerts,
    optionally scoped to a specific chain.
    """

    # Owner always allowed
    if user_id == settings.OWNER_CHAT_ID:
        return True

    tier = await get_tier(user_id)

    if tier not in TIER_CHAINS:
        return False

    if chain is None:
        return True

    return chain in TIER_CHAINS[tier]
