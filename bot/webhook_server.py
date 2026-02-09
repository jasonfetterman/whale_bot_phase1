from aiohttp import web
from services.stripe_webhook import handle_stripe_event

async def stripe_webhook(request: web.Request):
    payload = await request.read()
    sig = request.headers.get("Stripe-Signature")

    handle_stripe_event(payload, sig)
    return web.Response(text="ok")


def create_app():
    app = web.Application()
    app.router.add_post("/stripe/webhook", stripe_webhook)
    return app
