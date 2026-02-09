import stripe
from services.user_tiers import set_tier
from config.settings import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def handle_stripe_event(payload: bytes, sig_header: str):
    event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET,
    )

    # Subscription created or updated
    if event["type"] in (
        "checkout.session.completed",
        "customer.subscription.created",
        "customer.subscription.updated",
    ):
        data = event["data"]["object"]

        # We attach telegram_id + tier in metadata
        metadata = data.get("metadata", {})
        tg_id = metadata.get("telegram_id")
        tier = metadata.get("tier")

        if tg_id and tier:
            set_tier(int(tg_id), tier)

    return True
