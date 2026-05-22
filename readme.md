# RAG Workspace

A production-ready FastAPI project for **Retrieval-Augmented Generation (RAG)** applications with MongoDB integration, file processing, and intelligent text chunking.

## Features

- FastAPI async web framework with automatic API documentation
- MongoDB integration using `motor` (async MongoDB driver)
- File upload and validation (PDF, TXT, MD)
- Intelligent text chunking using LangChain
- Project-based file organization
- Docker Compose for MongoDB database
- Structured logging
- Environment-based configuration with Pydantic Settings
- Clean architecture: controllers, models, routes separation

## Project Structure

```
src/
├── main.py                  # FastAPI app entry point with MongoDB lifespan
├── docker-compose.yml       # MongoDB container setup
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
│
├── assets/
│   └── files/              # Uploaded files storage (ignored by git)
│
├── controllers/            # Business logic layer
│   ├── BaseController.py       # Base controller with utilities
│   ├── DataController.py     # File validation & path generation
│   ├── ProcessController.py   # File loading & text chunking
│   └── ProjectController.py   # Project directory management
│
├── models/                 # Database models & schemas
│   ├── BaseDataModel.py       # Base model with DB connection
│   ├── ProjectModel.py        # Project CRUD operations
│   ├── ChunkModel.py          # Data chunk CRUD operations
│   ├── db_schemes/            # Pydantic data schemas
│   │   ├── project.py
│   │   └── data_chunk.py
│   └── enums/                 # Enumerations
│       ├── DataBaseEnum.py
│       ├── ProcessEnums.py
│       └── ResponseEnums.py
│
├── routes/                 # API endpoints
│   ├── base.py                # App info endpoint
│   ├── data.py                # Upload & process endpoints
│   └── schemes/
│       └── data.py            # Request/response schemas
│
├── helpers/                # Utilities
│   └── config.py              # Settings & environment config
│
└── DataBase/
    └── Dockerfile             # MongoDB image setup
```

## Setup

### 1. Clone and Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
cd src
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and add your API keys and configuration
```

### 4. Start MongoDB (using Docker)

```bash
cd src
docker-compose up -d
```

This starts MongoDB with:
- Port: `27017`
- Username: `admin`
- Password: `password123`

### 5. Run the Application

```bash
cd src
fastapi dev main.py
```

Or for production:

```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `APP_NAME` | Application name | `RAG API` |
| `APP_VERSION` | Application version | `1.0.0` |
| `OPENAPI_URL` | OpenAPI schema URL | `/openapi.json` |
| `OPENAI_API_KEY` | OpenAI API key (for future LLM integration) | `sk-...` |
| `FILE_ALLOW_EXTS` | Allowed file extensions for upload | `["application/pdf", "text/plain", "text/markdown"]` |
| `MAX_FILE_SIZE_MB` | Maximum file upload size in MB | `10` |
| `FILE_DEFAULT_CHUNK_SIZE` | File read chunk size in bytes | `1024` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://admin:password123@localhost:27017` |
| `MONGODB_DB_NAME` | MongoDB database name | `rag_db` |

## API Endpoints

### Base Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/` | Get application info (name, version) |
| `GET` | `/docs` | Swagger UI documentation |
| `GET` | `/redoc` | ReDoc documentation |

### Data Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/data/upload/{project_id}` | Upload a file to a project |
| `POST` | `/api/data/process/{project_id}` | Process a file into text chunks |

#### Upload File

```bash
curl -X POST \
  http://localhost:8000/api/data/upload/my-project \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "signal": "file_upload_success",
  "file id": "abc123_document.pdf",
  "project id": "..."
}
```

#### Process File

```bash
curl -X POST \
  http://localhost:8000/api/data/process/my-project \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "abc123_document.pdf",
    "chunk_size": 100,
    "overlap_size": 20,
    "do_reset": 0
  }'
```

**Response:** Array of text chunks with metadata

## Architecture Overview

### File Processing Pipeline

1. **Upload** → File is validated (type, size) and saved to `assets/files/{project_id}/`
2. **Process** → File is loaded using appropriate loader (PyPDFLoader, TextLoader)
3. **Chunk** → Content is split using LangChain's RecursiveCharacterTextSplitter
4. **Store** → (Future) Chunks will be stored in MongoDB for retrieval

### Supported File Types

- **PDF** (`.pdf`) — via PyMuPDF
- **Text** (`.txt`) — via TextLoader
- **Markdown** (`.md`) — via TextLoader

## Development

### Adding New File Types

Edit `src/models/enums/ProcessEnums.py` and `src/controllers/ProcessController.py` to add new file loaders.

### Database Models

All models extend `BaseDataModel` and use async MongoDB operations:

- `ProjectModel` — Create, get, or list projects
- `ChunkModel` — Insert single or batch chunks

## Notes

- Uploaded files are stored in `src/assets/files/` and are **ignored by git** (see `src/assets/files/.gitignore`)
- MongoDB data persists in a Docker volume (`mongo-data`)
- The project uses structured logging for all operations

## License

MIT
