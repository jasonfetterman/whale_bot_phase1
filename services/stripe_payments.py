# FILE: services/stripe_payments.py
# LOCATION: services/stripe_payments.py
# DROP-IN REPLACEMENT

import stripe
from config.settings import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(
    *,
    tier: str,
    success_url: str,
    cancel_url: str,
    telegram_id: int,
) -> str:
    """
    Create a Stripe Checkout session and return the URL.
    """

    price_map = {
        "pro": settings.STRIPE_PRICE_PRO,
        "elite": settings.STRIPE_PRICE_ELITE,
        "super_elite": settings.STRIPE_PRICE_SUPER_ELITE,
    }

    price_id = price_map.get(tier)
    if not price_id:
        raise RuntimeError(f"Unknown tier: {tier}")

    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "telegram_id": str(telegram_id),
            "tier": tier,
        },
    )

    return session.url
