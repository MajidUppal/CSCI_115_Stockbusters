# AC215 MS2 — Containerized RAG (FastEmbed + Chroma + FastAPI)

A minimal, reproducible RAG pipeline:

- **Ingest:** load `.pdf` / `.txt` / `.md` → normalize text (removes `\n`, fixes quotes/dashes) → split into chunks → embed with **FastEmbed (BAAI/bge-small-en-v1.5)** → upsert into **Chroma** (persisted).
- **API:** query the vector store and return top-k chunks (text + metadata + distance).

---

## Project layout

ac215-ms2/
├─ data/ # ← Put your source docs here (.pdf, .txt, .md)
├─ artifacts/
│ ├─ sanitized/ # ← Sanitized text snapshots (per page/file)
│ ├─ ingest_summary.json # run metadata
│ ├─ metadata.json # model/chunk settings summary
│ └─ retrieval_sample.json # sample retrieval at ingest time
├─ volumes/
│ └─ chroma/ # ← Persisted Chroma DB (vectors + metadata)
├─ services/
│ ├─ ingest/
│ │ ├─ Dockerfile
│ │ ├─ pyproject.toml
│ │ └─ src/
│ │ ├─ build_index.py # entrypoint: runs full ingestion pipeline
│ │ ├─ load_docs.py # loaders & sanitization (removes \n)
│ │ ├─ split_chunk.py # chunking
│ │ └─ settings.py # ingest config
│ └─ api/
│ ├─ Dockerfile
│ ├─ pyproject.toml
│ └─ src/
│ ├─ server.py # FastAPI app (/health, /query)
│ ├─ retriever.py # Chroma client + embedding for queries
│ └─ settings.py # api config
├─ docker-compose.yml
├─ .env # runtime configuration (copied from .env.example)
└─ README.md


---

## Prerequisites

- **Windows PowerShell**
- **Docker Desktop** (WSL2 backend recommended)
- Internet access (first run downloads the ONNX embedding model, ~70–100 MB)

---

## Configuration

Copy the example env and adjust if needed:

```powershell
Copy-Item .\.env.example .\.env -Force

# Paths
VECTOR_STORE_PATH=/chroma
VECTOR_COLLECTION=stocks_rag_v1
DATA_DIR=/app/data
ARTIFACTS_DIR=/app/artifacts

# Chunking
CHUNK_SIZE=800
CHUNK_OVERLAP=150

# Embedding model
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# API
API_HOST=0.0.0.0
API_PORT=8000



## Quick start
`powershell
# -1) put a few .txt/.md files under ./data

# 0) (Optional) Clean any old state
docker compose down -v
Remove-Item -Recurse -Force .\volumes\chroma, .\artifacts -ErrorAction SilentlyContinue

# 1) Build images (api + ingest)
docker compose build --no-cache

# 2) Ingest (one-off job): parses data/, chunks, embeds, writes to Chroma + artifacts/
docker compose run --rm ingest python -m src.build_index

# 3) Start the API
docker compose up -d api

# 4) Health check
curl http://localhost:8000/health

# 5) Query (PowerShell pretty JSON)
irm -Method Post -Uri "http://localhost:8000/query" `
  -ContentType "application/json" `
  -Body (@{ q = "Explain P/E ratio"; k = 5 } | ConvertTo-Json) | ConvertTo-Json -Depth 6


