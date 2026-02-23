from dotenv import load_dotenv
load_dotenv(override=True)

from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationError
import sys


class Settings(BaseSettings):
    # Core
    BOT_TOKEN: str
    OWNER_CHAT_ID: int

    # Alchemy
    ALCHEMY_KEY: str

    # Global fallback (USD)
    WHALE_USD_THRESHOLD: float = 500_000

    # Per-chain thresholds
    ETH_WHALE_THRESHOLD: float = 100
    BSC_WHALE_THRESHOLD: float = 500
    POLYGON_WHALE_THRESHOLD: float = 1_000_000
    ARBITRUM_WHALE_THRESHOLD: float = 200
    BASE_WHALE_THRESHOLD: float = 150

    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_PRICE_PRO: str
    STRIPE_PRICE_ELITE: str
    STRIPE_PRICE_SUPER_ELITE: str
    STRIPE_WEBHOOK_SECRET: str
    
    WEBHOOK_BASE_URL: str
    WEBHOOK_PORT: int = 3000


    class Config:
        env_file = ".env"
        extra = "forbid"

    # ---- validators ----

    @field_validator("BOT_TOKEN")
    @classmethod
    def bot_token_valid(cls, v: str):
        if not v.startswith(""):
            raise ValueError("BOT_TOKEN invalid")
        return v

    @field_validator("ALCHEMY_KEY")
    @classmethod
    def alchemy_key_valid(cls, v: str):
        if len(v) < 10:
            raise ValueError("ALCHEMY_KEY looks invalid")
        return v

    @field_validator("STRIPE_SECRET_KEY")
    @classmethod
    def stripe_key_valid(cls, v: str):
        if not (v.startswith("sk_test_") or v.startswith("sk_live_")):
            raise ValueError("STRIPE_SECRET_KEY must be test or live key")
        return v

    @property
    def STRIPE_MODE(self) -> str:
        return "live" if self.STRIPE_SECRET_KEY.startswith("sk_live_") else "test"


try:
    settings = Settings()
except ValidationError as e:
    print("\n❌ CONFIG ERROR — FIX .env BEFORE RUNNING:\n")
    print(e)
    sys.exit(1)
