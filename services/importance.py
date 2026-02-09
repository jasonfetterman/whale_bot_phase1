def score_importance(amount: float, threshold: float) -> str:
    """
    Returns a human-readable importance label
    based on how far above threshold the transfer is.
    """

    if threshold <= 0:
        return "Notable transfer"

    ratio = amount / threshold

    if ratio >= 10:
        return "🔥 Extreme (Top ~1%)"
    if ratio >= 5:
        return "🚨 Very High (Top ~3%)"
    if ratio >= 3:
        return "⚠️ High (Top ~5%)"
    if ratio >= 2:
        return "Notable (Above average)"

    return "Large transfer"
