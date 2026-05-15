# RAG Workspace

A FastAPI-based project template for building Retrieval-Augmented Generation (RAG) applications.

## Overview

This project provides a clean starting point for developing RAG-powered applications using FastAPI, with structured configuration management via Pydantic Settings and environment-based secrets handling.

## Features

- ⚡ **FastAPI** - Modern, fast web framework for building APIs
- ⚙️ **Pydantic Settings** - Type-safe configuration with `.env` file support
- 🔐 **Environment-based secrets** - Secure API key management
- 📁 **Modular structure** - Organized routes, helpers, and models directories

## Project Structure

```
RAG-workspace/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── .env.example         # Environment template
├── routes/
│   └── base.py          # API routes
├── helpers/
│   ├── __init__.py
│   └── config.py        # Configuration and settings
└── models/              # Data models (Pydantic/SQLAlchemy)
```

## Prerequisites

- Python 3.8+
- pip

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd RAG-workspace
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your actual API keys:
   ```env
   APP_NAME=RAG-workspace
   APP_VERSION=0.1.0
   OPENAPI_URL=/openapi.json
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

Start the development server:

```bash
fastapi dev main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint    | Description                |
|--------|-------------|----------------------------|
| GET    | `/api/`     | App info (name & version)  |
| GET    | `/docs`     | Swagger UI documentation   |
| GET    | `/redoc`    | ReDoc documentation        |

## Environment Variables

| Variable          | Description                          | Required |
|-------------------|--------------------------------------|----------|
| `APP_NAME`        | Application name                     | Yes      |
| `APP_VERSION`     | Application version                  | Yes      |
| `OPENAPI_URL`     | OpenAPI schema URL path              | Yes      |
| `OPENAI_API_KEY`  | OpenAI API key for RAG features      | Yes      |

## Future Enhancements

- [ ] Vector database integration (Pinecone, Weaviate, Chroma)
- [ ] Document ingestion endpoints (PDF, TXT, DOCX)
- [ ] OpenAI embeddings integration
- [ ] Chat/completion endpoints with context retrieval
- [ ] Conversation history management

## License

[MIT](LICENSE) - feel free to use and modify for your own projects.

---

Built with ❤️ using FastAPI.
