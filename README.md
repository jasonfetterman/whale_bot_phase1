🐋 WhalerX — Crypto Whale Tracking Telegram Bot (Phase 1)

WhalerX is a real-time crypto whale tracking Telegram bot built to monitor large on-chain Ethereum transactions and deliver instant alerts to subscribed users.

This repository contains the Telegram bot service only.

Payments, authentication, subscription management, and plan upgrades are handled by a separate Next.js web application.

🚀 Core Features
📡 Real-Time Whale Monitoring

Ethereum mainnet monitoring via Alchemy WebSocket

Large transaction detection

Instant Telegram delivery

👛 Wallet Management

Add / remove tracked wallets

Optional wallet labels

View all tracked wallets inside Telegram

Enable / disable alerts per wallet

Chain selection per wallet (Phase 1: Ethereum)

💳 Subscription System

Free / Pro / Elite / Super Elite tiers

Hard wallet limits enforced inside bot

Plan retrieved dynamically from web app

Automatic plan enforcement

Owner override (always Super Elite)

🔐 Account Linking

Telegram ↔ Web account linking via one-time code

Maps:

telegram_id ↔ clerk_user_id

Plan data fetched from web backend

🧱 System Architecture
Telegram Bot (Python / aiogram v3)
│
├── Wallet storage (SQLite / aiosqlite)
├── Whale alert delivery
├── Plan enforcement
├── Telegram ↔ Web linking
│
└── Web App (Next.js - Separate Repository)
    ├── Authentication (Clerk)
    ├── Subscriptions (Stripe)
    ├── Plan metadata storage
    └── API endpoints for bot plan verification
Important:

The bot does NOT process payments.

It only queries the web app API to determine a user's active plan.

🛠 Tech Stack

Python 3.11+

aiogram v3

SQLite (aiosqlite)

Alchemy WebSocket API

aiohttp (API communication)

Stripe (web app)

Clerk (web app authentication)

Next.js (separate repository)

⚙️ Local Setup
1️⃣ Clone Repository
git clone https://github.com/jasonfetterman/whale_bot_phase1.git
cd whale_bot_phase1
2️⃣ Create Virtual Environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\activate
3️⃣ Install Dependencies
pip install aiogram aiosqlite python-dotenv pydantic-settings stripe websockets aiohttp
🔑 Environment Variables

Create a .env file in the root directory:

BOT_TOKEN=your_telegram_bot_token
ALCHEMY_KEY=your_alchemy_api_key
OWNER_TG_ID=your_numeric_telegram_id
WEB_APP_BASE_URL=http://localhost:3000

⚠️ Never commit this file.

▶️ Run the Bot
.\.venv\Scripts\python.exe bot\main.py

You should see polling start without errors.

💎 Subscription Tiers
Plan	Wallet Limit
Free	1 wallet
Pro	10 wallets
Elite	50 wallets
Super Elite	Unlimited

Limits are enforced inside the bot using plan data fetched from the web application.

Owner account is automatically treated as Super Elite.

🧪 Phase 1 Scope

Ethereum whale monitoring

Multi-wallet tracking

Plan enforcement

Telegram ↔ Web linking

Local SQLite persistence

This repo does NOT include:

Web dashboard

Stripe webhooks

Clerk backend logic

📌 Roadmap

Multi-chain expansion

Custom alert thresholds per wallet

Usage analytics

Admin tools

Performance optimizations

Docker deployment

⚠️ Disclaimer

This project is for educational and informational purposes only.
It does not provide financial advice or investment recommendations.
