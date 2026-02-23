# FILE: services/plan_checker.py
# LOCATION: services/plan_checker.py
# DROP-IN REPLACEMENT

from services.user_tiers import get_tier

# Wallet limits per tier
WALLET_LIMITS = {
    "free": 1,
    "pro": 10,
    "elite": 50,
    "super_elite": float("inf"),
}


async def get_user_plan(telegram_id: int) -> str:
    return await get_tier(telegram_id)


async def can_track_wallets(telegram_id: int, current_count: int) -> bool:
    plan = await get_user_plan(telegram_id)
    limit = WALLET_LIMITS.get(plan, WALLET_LIMITS["free"])
    return current_count < limit
