# 🤖 AI Backend — FastAPI + OpenAI Agent

A production-ready FastAPI backend that proxies user messages to an OpenAI
agent, with JWT auth, OTP verification, Redis rate limiting, and PostgreSQL.

## ✨ Features
- ⚡ FastAPI (async) with lifespan-managed Redis pool
- 🤖 OpenAI Responses API integration (`gpt-4o-mini`)
- 🔐 JWT access/refresh tokens + invalidation store
- 📱 OTP via SMS (cool-down) and email
- 🛡️ Per-IP / per-user rate limiting middleware
- 🗄️ Async PostgreSQL (SQLAlchemy + asyncpg)
- ⚙️ Pydantic Settings with `.env`

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+

### Install
```bash
git clone https://github.com/norouzipouya05-sketch/AI_APP.git
cd ai_backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
# AI_APP
