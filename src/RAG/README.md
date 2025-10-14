# RAG — Containerized RAG (FastEmbed + Chroma + FastAPI)

A minimal, reproducible Retrieval-Augmented Generation (RAG) system:

- **Ingest:** load `.pdf` / `.txt` / `.md` → sanitize → chunk → embed with **FastEmbed** (default: `BAAI/bge-small-en-v1.5`) → upsert into **Chroma** (persisted).
- **API:** FastAPI endpoint to retrieve top-k chunks from the vector store.

---

## Project layout
```
RAG/
├─ data/ # your source docs (.pdf, .txt, .md)
├─ artifacts/ # sanitized text + ingest metadata
├─ volumes/
│ └─ chroma/ # persisted Chroma vector store
├─ docs/ # optional screenshots/notes for README
├─ rag.py # SINGLE Python file (CLI + pipeline + API)
├─ pyproject.toml # runtime dependencies
├─ Dockerfile # single image for ingest + serve
├─ docker-compose.yml # one service: rag
├─ .env.example # documented config sample
├─ .env # your local overrides (gitignored)
├─ .gitignore # ignore artifacts/volumes/.env, etc.
└─ README.md
```


---

## Prerequisites

- **Windows PowerShell** (run from the repo root)
- **Docker Desktop** (WSL2 backend recommended)
- Internet (first run downloads the ONNX embedding model, ~70–100 MB)

---

## Configuration

Create your local env file from the template:

```powershell
Copy-Item .\.env.example .\.env -Force

# API
API_PORT=8000

# Vector store
VECTOR_STORE_PATH=./volumes/chroma
VECTOR_COLLECTION=stocks_rag_v1

# Paths
DATA_DIR=./data
ARTIFACTS_DIR=./artifacts

# Chunking
CHUNK_SIZE=1200
CHUNK_OVERLAP=200

# Embedding model
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

## Quick start
`powershell
# -1) put a few .txt/.md files under ./data

# 0) (Optional) Clean any old state
docker compose down -v
Remove-Item -Recurse -Force .\volumes\chroma, .\artifacts -ErrorAction SilentlyContinue

# 1) Build & start the API 
docker compose up --build -d

# 2) Ingest text
docker compose run --rm rag --ingest

# 5) Query (PowerShell pretty JSON)
irm -Method Post -Uri "http://localhost:8000/query" `
  -ContentType "application/json" `
  -Body (@{ q = "Explain P/E ratio"; k = 5 } | ConvertTo-Json) | ConvertTo-Json -Depth 6


