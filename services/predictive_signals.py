from services.wallet_behavior import behavior_score

def soft_signal(profile: dict) -> str | None:
    """
    Generate non-predictive, observational signals.
    NO price targets. NO advice.
    """
    events = profile.get("events", 0)
    avg_usd = profile.get("avg_usd", 0) or 0
    max_usd = profile.get("max_usd", 0) or 0

    if events >= 5 and avg_usd >= 1_000_000:
        return "📈 Pattern: Repeated large transfers observed"

    if max_usd >= 10_000_000:
        return "⚠️ Pattern: Exceptionally large historical transfer"

    if events >= 3:
        return "🔁 Pattern: Wallet has repeated activity"

    return None
