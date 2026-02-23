🐋 WhalerX
Real-Time Crypto Whale Tracking Infrastructure

Phase 1 — Telegram Monitoring Engine












🌊 Overview

WhalerX is a real-time crypto whale monitoring infrastructure service designed to track large on-chain Ethereum transactions and deliver instant alerts to Telegram users.

This repository contains the Telegram monitoring engine only.

Authentication, billing, subscription management, and account dashboards are handled by a separate web application built with Next.js.

WhalerX is architected as a scalable, event-driven, async monitoring system.

🎯 Product Vision

WhalerX is built to become:

A multi-chain whale intelligence platform

A scalable SaaS subscription service

A real-time blockchain alerting engine

A modular backend capable of supporting web, mobile, and API clients

Phase 1 focuses on:

Ethereum monitoring

Subscription enforcement

Telegram delivery

🚀 Core Capabilities
📡 Real-Time Blockchain Monitoring

Ethereum mainnet WebSocket streaming via Alchemy

Event-driven async architecture

Large transaction detection logic

Immediate Telegram alert dispatch

👛 Wallet Intelligence System

Add tracked wallets

Remove tracked wallets

Optional wallet labels

View tracked wallets inside Telegram

Enable / disable alerts per wallet

Per-wallet chain selection (Ethereum in Phase 1)

💳 Subscription Enforcement Engine

Free / Pro / Elite / Super Elite tiers

Hard wallet limits enforced inside bot

Dynamic plan validation from backend API

Automatic upgrade / downgrade handling

Owner override (always Super Elite)

🔐 Secure Telegram ↔ Web Linking

One-time code generated in web dashboard

User submits code inside Telegram

Bot maps:

telegram_id ↔ clerk_user_id

Plan fetched before sensitive actions

The bot never processes payments directly.

🧱 High-Level Architecture

Telegram Bot (Python / aiogram v3)
│
├── Async Event Loop
├── Whale Monitoring Service
├── Wallet Management Service
├── Plan Enforcement Layer
├── Telegram Delivery Router
├── SQLite Persistence Layer
│
└── Web Application (Separate Repository)
    ├── Authentication (Clerk)
    ├── Stripe Subscriptions
    ├── Plan Metadata Storage
    └── REST API for Bot Plan Verification

🔁 Plan Verification Flow

User attempts wallet action

Bot queries Web App API

Web App returns active subscription tier

Bot checks wallet count

Bot allows or denies action

Owner ID automatically bypasses restrictions

🧠 Architectural Principles

Async-first design

Separation of concerns

Stateless alert logic

Externalized payment handling

Secure environment variable management

Backend-verified subscription enforcement

🛠 Technology Stack
Bot Layer

Python 3.11+

aiogram v3

aiosqlite

aiohttp

websockets

pydantic-settings

Blockchain Layer

Alchemy WebSocket API

Web Infrastructure (Separate Repo)

Next.js

Clerk Authentication

Stripe Billing

REST API

📂 Project Structure
whale_bot_phase1/
│
├── bot/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── database/
│   ├── models/
│   └── utils/
│
├── .env                # Not committed
├── requirements.txt
├── Dockerfile          # (Optional - see below)
└── README.md
⚙️ Local Development Setup (Windows PowerShell)
1️⃣ Clone Repository
git clone https://github.com/jasonfetterman/whale_bot_phase1.git
cd whale_bot_phase1
2️⃣ Create Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt

If requirements.txt does not exist:

pip install aiogram aiosqlite python-dotenv pydantic-settings stripe websockets aiohttp
🔑 Environment Variables

Create a .env file:

BOT_TOKEN=your_telegram_bot_token
ALCHEMY_KEY=your_alchemy_api_key
OWNER_TG_ID=your_numeric_telegram_id
WEB_APP_BASE_URL=http://localhost:3000

Never commit this file.

▶️ Run the Bot
.\.venv\Scripts\python.exe bot\main.py

Expected behavior:

Bot connects

WebSocket initializes

Polling begins

No runtime errors

🐳 Docker Deployment (Production Ready)

Create Dockerfile:

FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot/main.py"]

Build:

docker build -t whalerx-bot .

Run:

docker run --env-file .env whalerx-bot
💎 Subscription Tiers
Plan	Wallet Limit
Free	1 wallet
Pro	10 wallets
Elite	50 wallets
Super Elite	Unlimited

Limits are enforced server-side via backend plan verification.

📊 Performance Considerations

Async architecture prevents blocking

WebSocket streaming minimizes latency

SQLite suitable for early-stage deployment

Designed for migration to PostgreSQL in future phases

Stateless alert handling allows horizontal scaling

🔒 Security Model

No private keys stored

No transaction signing

No payment handling

No secrets committed

All configuration via environment variables

Plan verification handled via backend API

🛣 Roadmap

Phase 2:

Multi-chain support (Base, Arbitrum, BSC)

Custom transaction thresholds

Advanced filtering

Alert categorization

Phase 3:

Web dashboard alert management

Historical whale analytics

Admin monitoring tools

Usage metrics & billing analytics

Phase 4:

Horizontal scaling

Distributed monitoring workers

Queue-based alert processing

Dedicated alert API

📸 Screenshots (Recommended Addition)

Add screenshots of:

Telegram alert example

Wallet list interface

Linking confirmation message

Create /assets/ folder and include images.

🤝 Contributing

Contributions are welcome.

Fork the repository

Create feature branch

Submit pull request

Ensure no secrets are committed

📜 License

MIT License

⚠️ Disclaimer

This software is provided for educational and informational purposes only.
It does not provide financial advice or investment recommendations.

Use at your own risk.
