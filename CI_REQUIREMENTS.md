# CI Requirements - What You Need to Run the RAG CI Pipeline

## Summary

The RAG CI pipeline is designed to run **without any external dependencies or secrets**. Everything needed is either:
- Built into GitHub Actions
- Created as dummy files during CI
- Mocked in tests

---

## ✅ Required: GitHub Repository Setup

### 1. GitHub Actions Enabled
- **Status:** ✅ Automatic (enabled by default)
- **What it does:** Runs workflows on push/PR
- **No action needed**

### 2. Workflow File Location
- **File:** `.github/workflows/ci-rag.yml`
- **Must exist:** Yes
- **Triggers:** Push/PR to `src/rag/**` or manual trigger

### 3. GitHub Actions Permissions
- **Default permissions:** ✅ Sufficient
- **Contents:** `read` (to checkout code)
- **Pull requests:** `read` (to comment on PRs)
- **No special permissions needed**

---

## ✅ Required: Repository File Structure

The CI expects the following files to exist:

### Core RAG Files (Required)
```
src/rag/
├── pyproject.toml          # Python dependencies
├── rag.py                  # Main RAG application
├── rag_helpers.py          # Helper functions
├── rag_functions.py        # RAG functions
├── Dockerfile              # Container definition
├── docker-entrypoint.sh    # Container entrypoint
├── docker-shell.sh         # Dev shell helper
└── pytest.ini             # Pytest configuration
```

### Test Files (Required)
```
src/rag/tests/
├── __init__.py
├── conftest.py             # Pytest fixtures
├── unit/
│   ├── __init__.py
│   ├── test_rag_core.py
│   ├── test_rag_helpers.py
│   └── test_retriever.py
├── integration/
│   ├── __init__.py
│   └── test_rag_api.py
└── system/
    ├── __init__.py
    └── test_rag_system.py
```

### Data Files (Optional but Recommended)
```
src/rag/data/
└── *.pdf, *.csv, etc.     # Sample data for testing
```

### Secrets (Auto-Created if Missing)
```
secrets/
└── gcs-key.json           # Created as {} if missing
```

---

## ✅ Required: Python Dependencies

All dependencies are defined in `src/rag/pyproject.toml`:

### Runtime Dependencies
- `fastapi>=0.111` - API framework
- `uvicorn[standard]>=0.30` - ASGI server
- `chromadb>=1.0.0` - Vector database
- `fastembed>=0.3.4,<0.4` - Embeddings
- `numpy>=1.26` - Numerical operations
- `pymupdf>=1.24.0,<1.25` - PDF parsing
- `google-cloud-storage>=2.10.0` - GCS (optional)
- `tiktoken>=0.7.0` - Token counting
- `orjson>=3.10.0` - JSON parsing

### Dev Dependencies (for CI)
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `pytest-asyncio>=0.21.0` - Async test support
- `black>=23.0.0` - Code formatter
- `flake8>=6.0.0` - Linter
- `httpx>=0.24.0` - FastAPI TestClient
- `requests>=2.31.0` - HTTP requests for system tests
- `pre-commit>=3.6.0` - Pre-commit hooks

**Note:** All dependencies are installed automatically by the Dockerfile.

---

## ❌ NOT Required: External Services

The CI is designed to run **without** these:

### ❌ Google Cloud Storage (GCS)
- **Status:** Optional
- **CI behavior:** Uses empty `GCS_BUCKET_NAME=""`
- **Dummy file:** Creates `secrets/gcs-key.json` as `{}` if missing
- **Tests:** Mocked or skipped

### ❌ ChromaDB External Instance
- **Status:** Not needed
- **CI behavior:** `AUTO_START_CHROMADB=0` (tests use mocks)
- **System tests:** Run against containerized server

### ❌ External APIs
- **Status:** None required
- **Tests:** Use mocks and fixtures

### ❌ Database Connections
- **Status:** None required
- **Tests:** Mocked

---

## ❌ NOT Required: GitHub Secrets

### Optional Secrets (CI works without them)

#### `SLACK_WEBHOOK_URL` (Optional)
- **Purpose:** Send Slack notifications on CI completion
- **Required:** No
- **CI behavior:** Checks if exists, skips if not
- **Location:** Workflow checks `if [ -n "${{ secrets.SLACK_WEBHOOK_URL }}" ]`
- **To enable:** Add secret in repo settings → Secrets and variables → Actions

#### `GCS_KEY_JSON` (Optional)
- **Purpose:** Real GCS credentials for production
- **Required:** No (CI creates dummy file)
- **CI behavior:** Creates `secrets/gcs-key.json` as `{}` if missing

---

## ✅ Environment Variables (Set by CI)

The CI workflow sets these automatically:

```bash
# ChromaDB settings
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
VECTOR_COLLECTION=test_collection

# GCS (disabled in CI)
GCS_BUCKET_NAME=""
GOOGLE_APPLICATION_CREDENTIALS=""

# Embedding model
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# Feature flags
ENABLE_CACHE=0
AUTO_START_CHROMADB=0
DEV=1

# System tests
API_BASE_URL=http://localhost:9000
```

**No action needed** - CI sets these automatically.

---

## ✅ GitHub Actions Features Used

### Built-in Actions (No Setup Needed)
- `actions/checkout@v4` - Checkout code
- `docker/setup-buildx-action@v3` - Docker Buildx
- `docker/build-push-action@v5` - Docker build with cache
- `actions/upload-artifact@v4` - Upload Docker image
- `actions/download-artifact@v4` - Download Docker image

### GitHub Actions Features
- **Runner:** `ubuntu-latest` (provided by GitHub)
- **Docker:** Pre-installed on runners
- **Cache:** GitHub Actions cache (`type=gha`)
- **Artifacts:** For sharing Docker image between jobs
- **Concurrency:** Prevents duplicate runs

---

## 🚀 How to Trigger CI

### Automatic Triggers
1. **Push to `src/rag/**`** on `main` or `develop` branches
2. **Pull request** targeting `main` or `develop` with changes to `src/rag/**`

### Manual Trigger
1. Go to **Actions** tab in GitHub
2. Select **RAG CI Pipeline**
3. Click **Run workflow**
4. Select branch and click **Run workflow**

---

## 📋 CI Jobs Overview

The CI runs 6 jobs:

1. **Build** - Builds Docker image with caching
2. **Lint and Format** - Runs `black` and `flake8`
3. **Unit Tests** - Runs unit tests with coverage
4. **Integration Tests** - Runs integration tests
5. **System Tests** - Runs system tests against live server
6. **Test Summary** - Reports results

**All jobs run in parallel** (except they depend on `build` job).

---

## ⚠️ Common Issues and Solutions

### Issue: "secrets/gcs-key.json not found"
**Solution:** CI creates this automatically as `{}` if missing. No action needed.

### Issue: "Docker build fails"
**Solution:** Check that all required files exist in `src/rag/` directory.

### Issue: "Tests fail"
**Solution:** 
- Check test files exist in `src/rag/tests/`
- Verify `pytest.ini` exists
- Check `conftest.py` has proper fixtures

### Issue: "CI not triggering"
**Solution:**
- Ensure workflow file is in `.github/workflows/ci-rag.yml`
- Check you're pushing to `main` or `develop` branch
- Verify changes are in `src/rag/**` path

---

## ✅ Checklist: Ready to Run CI?

- [ ] Repository has `.github/workflows/ci-rag.yml`
- [ ] `src/rag/` directory exists with core files
- [ ] `src/rag/tests/` directory exists with test files
- [ ] `src/rag/pyproject.toml` has all dependencies
- [ ] `src/rag/Dockerfile` exists
- [ ] `src/rag/pytest.ini` exists
- [ ] (Optional) `secrets/gcs-key.json` exists (or CI will create dummy)
- [ ] (Optional) `SLACK_WEBHOOK_URL` secret configured for notifications

**That's it!** Push to GitHub and CI will run automatically.

---

## 📊 Expected CI Runtime

- **First run (no cache):** 8-12 minutes
- **Subsequent runs (with cache):** 6-9 minutes
- **System tests:** 1.5-3 minutes
- **Build job:** 1-4 minutes (depends on cache)

---

## 🔍 Verification Commands

To verify your setup locally before pushing:

```bash
# Check required files exist
ls src/rag/rag.py src/rag/pyproject.toml src/rag/Dockerfile
ls src/rag/tests/ src/rag/pytest.ini

# Validate YAML
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci-rag.yml'))"

# Check Dockerfile can build (optional, slow)
docker build -t rag-test -f src/rag/Dockerfile .
```

---

**Bottom Line:** The CI is designed to run with **zero external dependencies**. Just push your code to GitHub and it will run automatically! 🚀

