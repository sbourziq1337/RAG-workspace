# RAG Workspace

FastAPI project template for RAG applications.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

## Run

```bash
fastapi dev main.py
```

## Env Variables

| Variable | Description |
|----------|-------------|
| `APP_NAME` | App name |
| `APP_VERSION` | App version |
| `OPENAI_API_KEY` | OpenAI API key |

## Endpoints

- `GET /api/` - App info
- `GET /docs` - Swagger UI
