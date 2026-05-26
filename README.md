# SENSEX Options Algo Trading

Production-style Python/FastAPI algorithmic trading scaffold for BSE SENSEX Options using Dhan Broker.

## Features

- Market regime detection
- SENSEX options chain analysis
- Regime-aware strategy selection
- Paper/live mode toggle
- Risk management and circuit breakers
- FastAPI REST backend
- DhanHQ integration wrapper

## Safety

This repository does not contain broker credentials. Use environment variables only.

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.api.main:app --reload
```

## API

- `GET /health`
- `GET /state`
- `POST /run-once`

## Disclaimer

For education and engineering use. Test in paper mode before any live trading.
