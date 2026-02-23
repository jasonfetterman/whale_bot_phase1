# FILE: services/plan_guard.py
# LOCATION: services/plan_guard.py
# DROP-IN REPLACEMENT

from config.settings import settings
from services.user_tiers import get_tier

# ---- chain access by tier ----
TIER_CHAINS = {
    "free": {"eth"},
    "pro": {"eth", "bsc", "polygon"},
    "elite": {"eth", "bsc", "polygon", "arbitrum", "base"},
    "super_elite": {"eth", "bsc", "polygon", "arbitrum", "base"},
}

# ---- feature access by tier ----
# controls whether intel is GENERATED at all
TIER_FEATURES = {
    "free": set(),
    "pro": {"SMART"},
    "elite": {"SMART", "BEHAVIOR"},
    "super_elite": {"SMART", "BEHAVIOR", "FLOW"},
}


async def can_receive_alert(user_id: int, chain: str | None = None) -> bool:
    if user_id == settings.OWNER_CHAT_ID:
        return True

    tier = await get_tier(user_id)

    if tier not in TIER_CHAINS:
        return False

    if chain is None:
        return True

    return chain in TIER_CHAINS[tier]


async def can_generate_feature(user_id: int, feature: str) -> bool:
    """
    HARD gate: should this intel be generated at all?
    feature examples: SMART, BEHAVIOR, FLOW
    """
    if user_id == settings.OWNER_CHAT_ID:
        return True

    tier = await get_tier(user_id)
    return feature in TIER_FEATURES.get(tier, set())
