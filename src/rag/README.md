# RAG — Containerized Retrieval-Augmented Generation (FastEmbed + Chroma + FastAPI)

A minimal, reproducible Retrieval-Augmented Generation (RAG) system built with:
- FastEmbed for sentence embeddings (`BAAI/bge-small-en-v1.5`)
- Chroma for persistent vector storage
- FastAPI for serving queries
- Everything runs in a single Docker image

**Milestone 4 (MS4)**: This README provides comprehensive setup instructions, environment configuration, usage guidelines, and integration documentation as required for MS4 deliverables.

---
## Repository Structure

### Directory Layout

```
src/rag/
│
├── data/                      # Source documents for ingestion
│   └── *.pdf, *.txt, *.csv    # Financial documents, CSV explanations
│
├── artifacts/                  # Pipeline outputs and version tracking
│   ├── ingest_summary.json    # Ingestion statistics and version info
│   ├── metadata.json          # Version tracking and collection metadata
│   ├── chunk_stats.json       # Chunking parameters and statistics
│   ├── sample_vector.json     # Sample embedding for verification
│   └── sanitized/             # Cleaned text chunks (intermediate)
│
├── docs/                       # MS4 Documentation (NEW)
│   ├── APPLICATION_DESIGN.md  # Solution + Technical architecture
│   └── DATA_VERSIONING.md     # Data versioning strategy and instructions
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests (fast, no external deps)
│   │   ├── test_rag_core.py
│   │   ├── test_rag_internals.py
│   │   ├── test_retriever.py
│   │   ├── test_gcs_sync.py   # NEW: GCS sync tests
│   │   └── test_ingestion.py  # NEW: Ingestion pipeline tests
│   ├── integration/            # Integration tests (mocked services)
│   │   └── test_rag_api.py
│   ├── system/                 # System tests (require running server)
│   │   └── test_rag_system.py
│   └── conftest.py            # Pytest fixtures and configuration
│
├── rag.py                      # Main application (CLI + pipeline + API)
├── rag_helpers.py             # Utility functions for RAG connectivity
├── pyproject.toml             # Python dependencies and linting configs
├── pytest.ini                 # Pytest configuration
├── Dockerfile                 # Docker build configuration
├── docker-entrypoint.sh       # Container entrypoint script
├── env.template               # Environment variables template
├── uv.lock                    # Dependency lock file
└── README.md                  # This file
```

### Code Organization

The RAG component follows a **monolithic design** for MS3/MS4 with clear separation of concerns:

- **`rag.py`** (~2800 lines): Main application containing:
  - Document loading and text extraction
  - Semantic chunking implementation
  - Embedding generation and batch processing
  - ChromaDB integration and GCS sync
  - FastAPI application and endpoints
  - CLI interface

- **`rag_helpers.py`**: Standalone utility functions for:
  - GCS connectivity and ChromaDB setup
  - Query interface abstraction
  - Convenience wrappers for external consumers

- **`tests/`**: Organized by test type:
  - `unit/`: Fast unit tests with mocked dependencies
  - `integration/`: API integration tests
  - `system/`: End-to-end tests with running server

### Style Guide

- **Python**: PEP 8 compliance enforced by `black` and `flake8`
- **Line length**: 120 characters
- **Docstrings**: Google style
- **Type hints**: Used throughout for clarity

---
## Prerequisites

### Required Software
- **Docker Desktop** (with WSL2 backend on Windows)
- **Windows PowerShell** (or WSL / Bash on Linux/Mac)
- **Git** (for version control and cloning repository)

### Required Access
- **Google Cloud Platform (GCP)** account with:
  - GCS bucket access (for ChromaDB persistence)
  - Service account credentials (JSON key file)
- **Network access** to GCS APIs (for cloud storage sync)

### System Requirements
- **RAM**: Minimum 4GB, recommended 8GB+ for large document processing
- **Disk**: 5GB+ free space for Docker images and data
- **CPU**: Multi-core recommended for embedding generation

## Environment Configuration

### Setup Instructions

1. **Copy the environment template**:
   ```powershell
   Copy-Item src/rag/env.template src/rag/.env
   ```

2. **Edit `src/rag/.env`** and configure the following variables:

#### Required Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `GCS_BUCKET_NAME` | GCS bucket for ChromaDB persistence | `stock-busters-chroma-bucket` | **Yes** |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCS service account JSON | `/workspace/gcs-key.json` | **Yes** (in Docker) |
| `VECTOR_COLLECTION` | ChromaDB collection name | `stocks_rag_v1` | No (default provided) |
| `EMBEDDING_MODEL` | FastEmbed model identifier | `BAAI/bge-small-en-v1.5` | No (default provided) |

#### API Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | FastAPI server host | `0.0.0.0` |
| `API_PORT` | FastAPI server port | `9000` |
| `CHROMADB_HOST` | ChromaDB server host (internal) | `localhost` |
| `CHROMADB_PORT` | ChromaDB server port (internal) | `8000` |

#### Data and Artifacts

| Variable | Description | Default |
|----------|-------------|---------|
| `DATA_DIR` | Source documents directory | `/workspace/data` |
| `ARTIFACTS_DIR` | Output artifacts directory | `/workspace/artifacts` |

#### Performance Tuning

| Variable | Description | Default |
|----------|-------------|---------|
| `EMBED_BATCH` | Embedding batch size | `256` |
| `UPSERT_BATCH` | ChromaDB upsert batch size | `256` |
| `ENABLE_CACHE` | Enable query result caching | `1` (enabled) |
| `CACHE_SIZE` | Maximum cache entries | `1000` |

#### Ingestion Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `SKIP_EXISTING` | Skip already processed documents | `1` (enabled) |
| `ENABLE_SECTION_FILTER` | Enable chapter-aware filtering | `1` (enabled) |
| `AUTO_START_CHROMADB` | Auto-start ChromaDB server | `1` (enabled) |

### Complete Environment Example

See `src/rag/env.template` for the complete list of all available environment variables with detailed descriptions.

**Note**: ChromaDB data is persisted in GCS bucket. ChromaDB server runs in the container on port 8000 (internal), API runs on port 9000 (exposed).

---

## Setup Instructions

### Step 1: Navigate to Project Root

Ensure you are in the root directory of the repository:

```powershell
cd CSCI115-AI-Agent
```

### Step 2: Configure Environment

1. Copy the environment template:
   ```powershell
   Copy-Item src/rag/env.template src/rag/.env
   ```

2. Edit `src/rag/.env` and set:
   - `GCS_BUCKET_NAME`: Your GCS bucket name
   - Verify `GOOGLE_APPLICATION_CREDENTIALS` points to your service account key

3. Ensure `secrets/gcs-key.json` exists with your GCP service account credentials

### Step 3: Build Docker Image

Build the RAG service Docker image (build context is root directory):

```powershell
docker build -t rag-service:latest -f src/rag/Dockerfile .
```

**Build context**: Root directory (`.`)
**Dockerfile**: `src/rag/Dockerfile`
**Expected time**: 5-10 minutes (downloads dependencies, builds image)

### Step 4: Create Docker Network (First Time Only)

```powershell
docker network create rag-network
```

This network allows RAG service to communicate with the orchestrator service.

### Step 5: Run RAG Service

#### Option A: Full Pipeline (Ingest + Serve)

Run ingestion and start API server in one container:

```powershell
# Clean up any existing container
docker stop rag-service 2>$null
docker rm rag-service 2>$null

# Run with ingestion and serving
docker run -d --name rag-service --network rag-network -p 9000:9000 --env-file src/rag/.env rag-service:latest --ingest --serve
```

This will:
1. Download ChromaDB data from GCS (if available)
2. Start ChromaDB server internally
3. Ingest documents from `data/` directory
4. Upload ChromaDB data to GCS
5. Start FastAPI server on port 9000

#### Option B: Ingestion Only

Run only document ingestion (no API server):

```powershell
docker run --rm --network rag-network --env-file src/rag/.env rag-service:latest --ingest
```

#### Option C: API Server Only

Start only the API server (assumes data already ingested):

```powershell
docker run -d --name rag-service --network rag-network -p 9000:9000 --env-file src/rag/.env rag-service:latest --serve
```

### Step 6: Verify Service is Running

Check container status:
```powershell
docker ps | Select-String "rag-service"
```

Check logs:
```powershell
docker logs rag-service
```

Test health endpoint:
```powershell
irm -Uri "http://localhost:9000/health" | ConvertTo-Json
```

Expected response:
```json
{
  "status": "ok",
  "service": "rag-api",
  "chromadb": "connected",
  "collection": "stocks_rag_v1",
  "count": 100
}
```

### Step 7: Access API Documentation

Open in browser: http://localhost:9000/docs

Interactive Swagger UI for testing API endpoints.


## Usage Guidelines

### Running Locally

#### Development Workflow

1. **Make code changes** to `src/rag/rag.py` or `src/rag/rag_helpers.py`
2. **Rebuild image**: `docker build -t rag-service:latest -f src/rag/Dockerfile .`
3. **Restart container**: `docker restart rag-service` or stop/start with new image
4. **Check logs**: `docker logs -f rag-service`

#### Common Operations

**Ingest new documents**:
1. Add documents to `src/rag/data/`
2. Run: `docker run --rm --env-file src/rag/.env rag-service:latest --ingest`

**Query the API**:
```powershell
# Simple query
irm -Method Post -Uri "http://localhost:9000/query" `
  -ContentType "application/json" `
  -Body (@{ q = "What is ROE?"; k = 5 } | ConvertTo-Json) | ConvertTo-Json -Depth 6

# Text format (for orchestrator)
irm -Method Post -Uri "http://localhost:9000/query/text" `
  -ContentType "application/json" `
  -Body (@{ q = "Explain P/E ratio"; k = 3; format = "text" } | ConvertTo-Json) | ConvertTo-Json
```

**Stop and clean up**:
```powershell
docker stop rag-service
docker rm rag-service
```

**Copy artifacts to local**:
```powershell
docker cp rag-service:/workspace/artifacts ./src/rag/artifacts
```

### API Endpoints

| Endpoint | Method | Description | Request Body |
|----------|--------|-------------|--------------|
| `/health` | GET | Health check and collection stats | None |
| `/query` | POST | Full metadata query results | `{"q": "query text", "k": 5}` |
| `/query/text` | POST | Text format for orchestrator | `{"q": "query", "k": 3, "format": "text"}` |
| `/docs` | GET | Interactive API documentation | None |

### Command-Line Interface

The `rag.py` script supports the following CLI arguments:

```bash
python rag.py [OPTIONS]

Options:
  --ingest              Run document ingestion
  --serve               Start FastAPI server
  --target-tokens N     Target tokens per chunk (default: 900)
  --max-tokens N        Maximum tokens per chunk (default: 1400)
  --overlap-sentences N Number of sentences to overlap (default: 2)
  --sim-percentile F    Similarity percentile for splitting (default: 95.0)
  --max-depth N         Max recursion depth for chunking (default: 3)
```

Example:
```bash
docker run --rm --env-file src/rag/.env rag-service:latest --ingest --target-tokens 800 --max-tokens 1200
```

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
## Testing

### Running Tests Locally

#### Prerequisites
Ensure you have the dev dependencies installed:
```powershell
# In the container or local environment
pip install -e ".[dev]"
```

#### Run All Tests
```powershell
# From project root
cd src/rag
pytest
```

#### Run by Test Type
```powershell
# Unit tests only (fast, no external dependencies)
pytest tests/unit/ -v -m unit

# Integration tests (mocked services)
pytest tests/integration/ -v -m integration

# System tests (requires running server)
pytest tests/system/ -v -m system
```

#### Run with Coverage
```powershell
# Generate coverage report (target: ≥50%)
pytest --cov=rag --cov=rag_helpers --cov-report=term --cov-report=html --cov-fail-under=50

# View HTML report
# Open htmlcov/index.html in browser
```

#### Run Specific Test File
```powershell
pytest tests/unit/test_rag_core.py -v
```

### Test Markers

Tests are organized with pytest markers:
- `@pytest.mark.unit`: Unit tests (run quickly, no external deps)
- `@pytest.mark.integration`: Integration tests (require mocked services)
- `@pytest.mark.system`: System tests (require running server)
- `@pytest.mark.slow`: Tests that take significant time

### CI/CD Testing

Tests run automatically in GitHub Actions on every push/PR:
- **Build**: Docker image build verification
- **Lint**: `black` formatting and `flake8` code quality checks
- **Unit Tests**: Fast unit test suite
- **Integration Tests**: API integration tests with mocks
- **System Tests**: End-to-end tests with running server
- **Coverage**: Minimum 50% code coverage required

View CI status: `.github/workflows/ci-rag.yml`

---

## CI/CD

### Continuous Integration Pipeline

The RAG component has automated CI/CD via GitHub Actions (`.github/workflows/ci-rag.yml`).

#### What Runs in CI

| Job | Description | Triggers |
|-----|-------------|----------|
| **Build** | Docker image build and verification | Every push/PR to `src/rag/**` |
| **Lint & Format** | `black` formatting check, `flake8` linting | Every push/PR |
| **Unit Tests** | Fast unit test suite with coverage | Every push/PR |
| **Integration Tests** | API integration tests with mocked services | Every push/PR |
| **System Tests** | End-to-end tests with running server | Every push/PR |
| **Test Summary** | Aggregated test results and notifications | After all tests |

#### CI Triggers

- **Push** to branches: `main`, `develop`, `MS4`, `milestone4`
- **Pull requests** to above branches
- **Manual trigger** via `workflow_dispatch`

#### How to Check CI Status

1. **GitHub UI**: Go to repository → Actions tab → "RAG CI Pipeline"
2. **Commit status**: Green checkmark or red X on commits
3. **PR checks**: Status shown in pull request

#### CI Requirements

- ✅ **Build**: Docker image must build successfully
- ✅ **Lint**: No `black` or `flake8` errors
- ✅ **Tests**: All unit, integration, and system tests must pass
- ✅ **Coverage**: Minimum 50% code coverage

#### Local CI Simulation

Run CI checks locally before pushing:

```powershell
# Build check
docker build -t rag-service:latest -f src/rag/Dockerfile .

# Lint check
docker run --rm rag-service:latest black --check rag.py rag_helpers.py tests/
docker run --rm rag-service:latest flake8 --max-line-length=120 rag.py rag_helpers.py

# Test check
docker run --rm rag-service:latest pytest tests/ -v --cov=rag --cov=rag_helpers --cov-fail-under=50
```

---

## Integration with Orchestrator

The RAG service integrates with the orchestrator service (`src/agents/orchestrator/`) to provide financial knowledge during conversational AI interactions.

### Integration Architecture

```
┌──────────────────┐
│   Orchestrator   │  (LLM Agent)
│   Service        │
└────────┬─────────┘
         │ HTTP POST
         │ /query/text
         ▼
┌──────────────────┐
│   RAG Service    │  (Knowledge Base)
│   Port 9000      │
└──────────────────┘
```

### API Integration

#### Endpoint: `POST /query/text`

**Purpose**: Simplified text results for LLM consumption

**Request**:
```json
{
  "q": "What is ROE?",
  "k": 3,
  "format": "text"
}
```

**Response**:
```json
{
  "query": "What is ROE?",
  "answer": "Information 1: Return on Equity (ROE) measures...\n\nInformation 2: ROE is calculated as...",
  "found": true,
  "source_count": 3
}
```

### Network Configuration

#### Docker Network Setup

Both services should be on the same Docker network:

```powershell
# Create shared network (if not exists)
docker network create rag-network

# RAG service (already on network)
docker run -d --name rag-service --network rag-network -p 9000:9000 ...

# Orchestrator service (connect to same network)
docker run -d --name orchestrator --network rag-network ...
```

#### Environment Variables for Orchestrator

In orchestrator's `.env`:
```
RAG_API_URL=http://rag-service:9000
RAG_API_TIMEOUT=10
```

#### Health Check Integration

Orchestrator can check RAG health:
```powershell
irm -Uri "http://rag-service:9000/health"
```

Returns collection stats and connectivity status.

### Error Handling

The RAG API handles errors gracefully:
- **Connection errors**: Returns error message in response
- **Empty results**: Returns `"found": false` with helpful message
- **Timeouts**: Configurable via `RAG_API_TIMEOUT`

See orchestrator's `query_financial_knowledge_base()` function for integration example.

---

## Quick Reference

### Common Commands

| Operation | Command |
|-----------|---------|
| **Build image** | `docker build -t rag-service:latest -f src/rag/Dockerfile .` |
| **Run full pipeline** | `docker run -d --name rag-service --network rag-network -p 9000:9000 --env-file src/rag/.env rag-service:latest --ingest --serve` |
| **Ingest only** | `docker run --rm --env-file src/rag/.env rag-service:latest --ingest` |
| **API only** | `docker run -d --name rag-service -p 9000:9000 --env-file src/rag/.env rag-service:latest --serve` |
| **Query API** | `irm -Method Post -Uri "http://localhost:9000/query" -ContentType "application/json" -Body (@{q="test";k=5} \| ConvertTo-Json)` |
| **Stop service** | `docker stop rag-service; docker rm rag-service` |
| **View logs** | `docker logs -f rag-service` |
| **Run tests** | `pytest tests/ -v --cov=rag --cov=rag_helpers` |
| **Copy artifacts** | `docker cp rag-service:/workspace/artifacts ./src/rag/artifacts` |

---

## MS2/MS3 RAG Deliverables (Historical)

| **Deliverable**                                                                             | **Repository Location**              | **Description**                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Screenshot of running instances (cloud or local)**                                        | N/A (removed)                        | Screenshots showing Docker container(s) or local PowerShell instances running the RAG pipeline (e.g., build, run, query, and vector retrieval).                                                                                                                    |
| **Documentation and Build Instructions**                                                    | `RAG/Dockerfile` and `RAG/README.md` | Comprehensive documentation of the RAG pipeline design, architecture, configuration, and run instructions. Includes the Dockerfile used to build the containerized environment and the “Quick Start” guide for ingestion and API serving.                          |
| **pyproject.toml (using uv)**                                                               | `RAG/pyproject.toml`                 | Defines Python dependencies and environment configuration for the container (managed with **uv**).                                                                                                                                                                  |
| **Scripts or docker-compose.yml (when applicable)**                                         | `RAG/rag.py` *(main script)*         | `rag.py` acts as the unified CLI and pipeline script handling ingestion, chunking, embedding, vector storage, and API serving. *(No docker-compose.yml is required because the pipeline runs with a single Dockerfile command. docker-composed moved to _archived folder)*                                   |
| **Containerized RAG pipeline with scripts for chunking, vectorization, and DB integration** | `RAG/rag.py`                         | Implements ingestion, sanitization, text splitting, embedding (FastEmbed), and vector store integration (Chroma).                                                                                                            |
| **Pipeline Evidence and Logs**                                                              | `RAG/artifacts/`                     | Contains automatically generated outputs and logs verifying end-to-end pipeline execution — including chunking summaries (`metadata.json`), ingestion logs (`ingest_summary.json`), and sample embeddings (`sample_vector.json`). |
