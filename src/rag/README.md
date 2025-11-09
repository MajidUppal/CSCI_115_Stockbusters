# RAG — Containerized Retrieval-Augmented Generation (FastEmbed + Chroma + FastAPI)

A minimal, reproducible Retrieval-Augmented Generation (RAG) system built with:
- FastEmbed for sentence embeddings (`BAAI/bge-small-en-v1.5`)
- Chroma for persistent vector storage
- FastAPI for serving queries
Everything runs in a single Docker image
---
## RAG Layout
```
RAG/
│
├─ data/                  # source docs (.pdf, .txt, .md)
│
├─ artifacts/             # pipeline outputs
│  ├── ingest_summary.json # ingest summary
│  ├── metadata.json # metadata about ingested docs
│  ├── retrieval_sample.json # retrieval sample
│  └── sample_vector.json # vector embedding sample
│
├─ rag.py                 # SINGLE Python file (CLI + pipeline + API)
├─ pyproject.toml         # runtime dependencies
├─ Dockerfile             # single image for ingest + serve
├─ .env                   # local config 
├─ uv.lock                # uv lock file
└─ README.md
```
---
## Prerequisites
- Windows PowerShell (or WSL / Bash)
- Docker Desktop (with WSL2 backend)

## Configuration
Your `.env` should contain (see `env.template` for full list):
```
API_PORT=9000
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
VECTOR_COLLECTION=stocks_rag_v1
GCS_BUCKET_NAME=your-bucket-name
DATA_DIR=/workspace/data
ARTIFACTS_DIR=/workspace/artifacts
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
CHROMA_TELEMETRY_DISABLED=1
GOOGLE_APPLICATION_CREDENTIALS=/workspace/gcs-key.json
```
**Note**: ChromaDB data is persisted in GCS bucket. ChromaDB server runs in the container on port 8000, API runs on port 9000.
---

## Quick Start
1. Ensure you are in the root directory (`CSCI115-AI-Agent`) as your working directory

Example:
```
cd CSCI115-AI-Agent
```
2. Optional: Clean up any old container name
```
docker stop rag-service 2>$null
docker rm rag-service 2>$null
```
3. Build the image (build context: root directory)
```
docker build -t rag-service:latest -f src/rag/Dockerfile .
```
4. Run everything (Ingest + Serve in one container)
```
docker network create rag-network 2>$null
docker run -d --name rag-service --network rag-network -p 9000:9000 --env-file src/rag/.env rag-service:latest --ingest --serve
```


This:
- Ingests documents from `data/`
- Records chunking info in `artifacts/ingest_summary.json`
- Writes ingest metadata to `artifacts/metadata.json`
- Stores vectors in ChromaDB (persisted in GCS bucket)
- Starts ChromaDB server on port 8000 (internal)
- Starts the FastAPI server on port 9000

```
# For only ingestion (no querying)
docker run --rm --network rag-network --env-file src/rag/.env rag-service:latest --ingest
```
# Optional API:
Once running, open:  
http://localhost:9000/docs  
to see the interactive API docs.

## Query Example (PowerShell pretty JSON)
After the container is running, run this from another PowerShell window:
```
irm -Method Post -Uri "http://localhost:9000/query" -ContentType "application/json" -Body (@{ q = "Explain P/E ratio"; k = 5 } | ConvertTo-Json) | ConvertTo-Json -Depth 6
```
Example output:
```
{
  "query": "Explain P/E ratio",
  "results": [
    {
      "doc": "The P/E ratio (price-to-earnings ratio) measures how much investors are willing to pay per dollar of earnings...",
      "score": 0.88,
      "source": "PrinciplesofFinanceSample.pdf"
    }
  ]
}
```

## Dump a Sample Vector
```
docker run --rm --network rag-network --env-file src/rag/.env rag-service:latest --dump-vector
```
This saves:
artifacts/sample_vector.json  
Example contents:
```
{
  "collection": "stocks_rag_v1",
  "id": "chunk_0001",
  "vector_dim": 384,
  "vector": [0.0123, -0.0058, 0.0449, ...]
}
```

## Stop the container
If you ran it detached (with -d), stop it with:  
```
docker stop rag-service
docker rm rag-service
```

## Copy artifacts to local
```
docker cp rag-service:/workspace/artifacts .\artifacts
```
**Note**: ChromaDB data is stored in GCS bucket, not in local volumes.

---
---
## Integration with Orchestrator

The RAG service integrates with the orchestrator service (`src/agents/orchestrator/`) via the `/query/text` endpoint. The orchestrator uses the RAG service to answer financial questions during conversations.

See `INTEGRATION_CHANGES.md` for details on the integration.

## Summary
| Step              | Command                                                                                                                             | Purpose                                  |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| Build image       | `docker build -t rag-service:latest -f src/rag/Dockerfile .`                                                                        | Build the image (build context: root)    |
| Run end-to-end    | `docker run -d --name rag-service --network rag-network -p 9000:9000 --env-file src/rag/.env rag-service:latest --ingest --serve`   | Ingest & serve in one persistent container |
| Run ingest only   | `docker run --rm --network rag-network --env-file src/rag/.env rag-service:latest --ingest`                                         | Run ingestion only                       |
| Run API only      | `docker run -d --name rag-service --network rag-network -p 9000:9000 --env-file src/rag/.env rag-service:latest --serve`            | Start the FastAPI server only            |
| Query             | (PowerShell) `irm -Method Post -Uri "http://localhost:9000/query" -ContentType "application/json" -Body (@{ q = "Explain P/E ratio"; k = 5 } | ConvertTo-Json) | ConvertTo-Json -Depth 6` | Query the API                              |
| Stop API          | `docker stop rag-service; docker rm rag-service`                                                                                    | Stop container                            |
| Copy artifacts    | `docker cp rag-service:/workspace/artifacts .\artifacts`                                                                            | Copy results to host (data in GCS)       |


---

## MS2 RAG Deliverables

| **Deliverable**                                                                             | **Repository Location**              | **Description**                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Screenshot of running instances (cloud or local)**                                        | N/A (removed)                        | Screenshots showing Docker container(s) or local PowerShell instances running the RAG pipeline (e.g., build, run, query, and vector retrieval).                                                                                                                    |
| **Documentation and Build Instructions**                                                    | `RAG/Dockerfile` and `RAG/README.md` | Comprehensive documentation of the RAG pipeline design, architecture, configuration, and run instructions. Includes the Dockerfile used to build the containerized environment and the “Quick Start” guide for ingestion and API serving.                          |
| **pyproject.toml (using uv)**                                                               | `RAG/pyproject.toml`                 | Defines Python dependencies and environment configuration for the container (managed with **uv**).                                                                                                                                                                  |
| **Scripts or docker-compose.yml (when applicable)**                                         | `RAG/rag.py` *(main script)*         | `rag.py` acts as the unified CLI and pipeline script handling ingestion, chunking, embedding, vector storage, and API serving. *(No docker-compose.yml is required because the pipeline runs with a single Dockerfile command. docker-composed moved to _archived folder)*                                   |
| **Containerized RAG pipeline with scripts for chunking, vectorization, and DB integration** | `RAG/rag.py`                         | Implements ingestion, sanitization, text splitting, embedding (FastEmbed), and vector store integration (Chroma).                                                                                                            |
| **Pipeline Evidence and Logs**                                                              | `RAG/artifacts/`                     | Contains automatically generated outputs and logs verifying end-to-end pipeline execution — including chunking summaries (`metadata.json`), ingestion logs (`ingest_summary.json`), and sample embeddings (`sample_vector.json`). |
