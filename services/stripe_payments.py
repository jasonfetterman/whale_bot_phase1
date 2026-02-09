import os


import stripe
from config.settings import settings

# Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Paid tiers
TIERS = {
    "pro": {
        "price_id": settings.STRIPE_PRICE_PRO,
        "name": "Whaler X Pro",
    },
    "elite": {
        "price_id": settings.STRIPE_PRICE_ELITE,
        "name": "Whaler X Elite",
    },
    "super_elite": {
        "price_id": settings.STRIPE_PRICE_SUPER_ELITE,
        "name": "Whaler X Super Elite",
    },
}

def create_checkout_session(
    tier: str,
    success_url: str,
    cancel_url: str,
    telegram_id: int,
) -> str:
    if tier not in TIERS:
        raise ValueError("Invalid tier")

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[
            {
                "price": TIERS[tier]["price_id"],
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "telegram_id": telegram_id,
            "tier": tier,
        },
    )

    return session.url
