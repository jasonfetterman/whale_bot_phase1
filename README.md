🐋 WhalerX Telegram Bot

WhalerX is a real-time crypto whale tracking Telegram bot that monitors large on-chain transactions and sends instant alerts.
It supports paid subscription tiers, automatic plan enforcement, and seamless linking with a web app for billing and account management.

This repository contains the Telegram bot only.
Payments, authentication, and plan management are handled by a separate web app.

✨ Features

📡 Real-time whale alerts (Ethereum + supported chains)

👛 Track multiple wallets with optional labels

🔔 Enable / disable alerts per wallet

⛓ Select which chains to monitor per wallet

📄 View all tracked wallets in Telegram

💳 Subscription tiers (Free / Pro / Elite / Super Elite)

🚫 Hard wallet limits enforced by plan

🔐 Telegram ↔ Web account linking

👑 Owner override (always Super Elite)

🧱 Architecture Overview
Telegram Bot (aiogram)
│
├── Wallet management
├── Alert delivery
├── Plan enforcement
├── Telegram account linking
│
└── Web App (Next.js)
    ├── Authentication (Clerk)
    ├── Subscriptions (Stripe)
    ├── Plan storage (Clerk metadata)
    └── API used by bot for plan checks


The bot never handles payments directly.
It queries the web app to determine each user’s plan.

🛠 Tech Stack

Python 3.11+

aiogram v3

SQLite / aiosqlite

Alchemy WebSocket API

Stripe (subscriptions)

Clerk (user & plan management)

Next.js web app (separate repo)

🚀 Getting Started
1️⃣ Clone the repository
git clone https://github.com/yourusername/whale_bot_phase1.git
cd whale_bot_phase1

2️⃣ Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

3️⃣ Install dependencies
pip install aiogram aiosqlite python-dotenv pydantic-settings stripe websockets aiohttp

⚙️ Configuration

Create a .env file in the project root (this file is not committed):

BOT_TOKEN=your_telegram_bot_token
ALCHEMY_KEY=your_alchemy_api_key
OWNER_TG_ID=your_telegram_numeric_id
WEB_APP_BASE_URL=http://localhost:3000

▶️ Running the Bot

From the project root:

.\.venv\Scripts\python.exe bot\main.py


You should see the bot start polling with no errors.

🔐 Subscription Plans (Example)
Plan	Wallet Limit
Free	1 wallet
Pro	10 wallets
Elite	50 wallets
Super Elite	Unlimited

Plans are enforced inside the bot based on data fetched from the web app.

🔗 Telegram ↔ Web Linking

User generates a link code in the web app

User sends the code to the Telegram bot

Bot links:

telegram_id ↔ clerk_user_id


Bot automatically enforces the correct plan

🧪 Development Notes

Owner account is always treated as super_elite

SQLite is used for local persistence

Webhooks & Stripe logic live in the web app, not here

This repo is safe to publish (no secrets committed)

📌 Roadmap

 Additional chains

 Alert thresholds per wallet

 Usage analytics

 Admin dashboards

 Bot performance optimizations

⚠️ Disclaimer

This project is for educational and informational purposes only.
It does not provide financial advice.
