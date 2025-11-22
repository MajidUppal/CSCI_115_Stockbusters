# Data Versioning and Reproducibility

## Overview

This document describes the data versioning strategy for the RAG component, which handles large vector embeddings, document chunks, and persistent ChromaDB state.

## Chosen Method: DVC (Data Version Control)

### Approach

The RAG system uses **DVC** for data versioning, which provides:
1. **Version control for large files**: ChromaDB vectors, embeddings, and artifacts
2. **Git integration**: DVC metadata files tracked in git
3. **Reproducibility**: Link data versions to code commits
4. **Team collaboration**: Shared remote storage (GCS/S3) with DVC tracking

### Justification

#### Why DVC?

**DVC is chosen for the following reasons:**

1. **Data Characteristics**
   - **Large binary files**: ChromaDB stores millions of vector embeddings (384-dim floats)
   - **Versioned datasets**: Source documents and vector databases need versioning
   - **Size**: Vector database can grow to 10GB+ (not suitable for git directly)
   - **DVC handles**: Large files via remote storage (GCS/S3) with git-tracked metadata

2. **Workflow Fit**
   - **Standard tool**: DVC is explicitly mentioned in MS4 requirements
   - **Git integration**: DVC metadata files are small and git-friendly
   - **Remote storage**: Uses GCS as remote storage backend
   - **Pipeline tracking**: Can track data dependencies in ML pipelines

3. **Reproducibility**
   - **Git commits**: DVC links data versions to git commits
   - **Metadata files**: `.dvc` files track data hashes and versions
   - **Clear history**: `dvc diff` and `dvc show` provide version history
   - **Team collaboration**: Shared remote storage with version control

4. **MS4 Alignment**
   - **Explicitly mentioned**: MS4 requirements reference DVC as an example
   - **Standard approach**: Common tool in ML/data science workflows
   - **Documentation**: Well-documented with clear usage patterns

## Version History and Tracking

### DVC Version Tracking

DVC tracks data versions through:

#### 1. DVC Metadata Files (`.dvc`)
- **Location**: Git-tracked `.dvc` files (e.g., `data/chromadb.dvc`, `artifacts/ingest_summary.json.dvc`)
- **Contains**: File/directory hashes, remote storage paths, file sizes
- **Purpose**: Links data files to git commits
- **Format**: YAML files with checksums and remote URLs

#### 2. Git Integration
- **DVC files in git**: Small `.dvc` metadata files committed to git
- **Data in remote**: Actual large files stored in GCS (configured as DVC remote)
- **Version linking**: Each git commit with `.dvc` changes represents a data version
- **History**: `git log` shows data version changes alongside code changes

#### 3. Remote Storage (GCS)
- **Location**: GCS bucket configured as DVC remote
- **Purpose**: Stores actual large data files (ChromaDB, embeddings)
- **Access**: DVC manages upload/download via `dvc push` and `dvc pull`
- **Managed by DVC**: GCS objects are managed by DVC, not manually tracked

### Version History Workflow

```
1. Developer runs: python rag.py --ingest
   ↓
2. Ingestion creates/updates data files:
   - ChromaDB vector database
   - Artifacts (ingest_summary.json, chunk_stats.json)
   ↓
3. Developer adds data to DVC tracking:
   dvc add data/chromadb artifacts/
   ↓
4. DVC creates .dvc metadata files with checksums
   ↓
5. Developer commits DVC files to git:
   git add data/chromadb.dvc artifacts/*.dvc
   git commit -m "Update RAG data v1.2"
   ↓
6. Push data to remote storage:
   dvc push
   ↓
7. Version history: 
   - git log data/chromadb.dvc (see data version changes)
   - dvc diff (compare data versions)
   - dvc show (view data details)
```

## Setup Instructions

### Initial DVC Setup

```bash
# 1. Install DVC
pip install dvc dvc-gcs  # or dvc-s3 for AWS

# 2. Initialize DVC in project root
dvc init

# 3. Configure remote storage (GCS example)
dvc remote add -d myremote gs://your-bucket-name/dvc-storage

# 4. Add large data files to DVC
cd src/rag
dvc add data/chromadb artifacts/

# 5. Commit DVC metadata files
git add data/chromadb.dvc artifacts/*.dvc .dvc/.gitignore
git commit -m "Add RAG data to DVC"
```

### Equivalent to "dvc pull"

To retrieve a specific version of the RAG data:

#### Option 1: Latest Version (Default)
```bash
# Pull latest data from DVC remote
dvc pull

# Or in Docker build/run
docker build -t rag-service:latest -f src/rag/Dockerfile .
docker run --rm --env-file src/rag/.env rag-service:latest
```

#### Option 2: Specific Git Commit Version
```bash
# 1. Checkout specific git commit
git checkout <commit-hash>

# 2. Pull corresponding data version
dvc pull

# 3. Verify data version
dvc show data/chromadb.dvc
```

#### Option 3: Manual DVC Commands
```bash
# List available data versions
git log --oneline data/chromadb.dvc

# Compare data versions
dvc diff HEAD~1 data/chromadb

# Show data details
dvc show data/chromadb.dvc
```

### Version Verification

```bash
# Check current DVC status
dvc status

# View data file info
dvc show data/chromadb.dvc

# Verify data integrity
dvc check

# Compare with remote
dvc diff data/chromadb
```

## LLM-Generated Data

### Pre-Trained Embeddings (No LLM Generation)

The RAG system uses **pre-trained embeddings** from BAAI (Beijing Academy of AI):
- **Model**: `BAAI/bge-small-en-v1.5`
- **Type**: Sentence transformer (not LLM-generated)
- **Training**: Pre-trained on diverse English text
- **No fine-tuning**: Model used as-is for reproducibility

### Prompt and Output Tracking

Since RAG does not generate LLM content (only retrieves from documents), there are no LLM prompts or outputs to version. The system:
1. **Ingests** existing financial documents
2. **Embeds** using pre-trained model
3. **Retrieves** relevant chunks for queries

No LLM generation occurs in the RAG pipeline.

## Reproducibility Guarantees

### What is Reproducible?

✅ **Fully Reproducible**:
- Ingestion process (same documents → same chunks)
- Embedding generation (deterministic pre-trained model)
- Chunking parameters (recorded in `chunk_stats.json`)
- Code version (git commit)
- Data version (DVC tracked)

⚠️ **Partially Reproducible**:
- Exact vector values (may vary slightly with ONNX runtime versions)
- ChromaDB internal structure (HNSW index may differ)
- Query results (semantic similarity is approximate)

### Reproducibility Workflow

To reproduce a specific RAG state:

1. **Checkout code version**: `git checkout <commit-hash>`
2. **Pull corresponding data**: `dvc pull`
3. **Verify data version**: `dvc show data/chromadb.dvc`
4. **Run ingestion** (if needed): `python rag.py --ingest`
5. **Verify**: Compare `artifacts/ingest_summary.json` with original

## Best Practices

### For Developers

1. **Always commit `.dvc` files**: After `dvc add`, commit the `.dvc` metadata files
2. **Use descriptive commit messages**: Include data version info in commits
3. **Pull before working**: Run `dvc pull` after `git pull` to sync data
4. **Push after updates**: Run `dvc push` after `dvc add` to update remote
5. **Track artifacts**: Add `artifacts/` to DVC for version tracking

### For CI/CD

1. **Install DVC**: `pip install dvc dvc-gcs` in CI environment
2. **Configure credentials**: Set up GCS credentials for DVC remote
3. **Pull data**: Run `dvc pull` before tests/ingestion
4. **Cache data**: Consider caching DVC data between CI runs

### Data Versioning Commands Reference

```bash
# Add data to DVC tracking
dvc add <file-or-dir>

# Push data to remote
dvc push

# Pull data from remote
dvc pull

# Check status
dvc status

# Compare versions
dvc diff <commit1> <commit2> <path>

# Show data info
dvc show <path>.dvc

# Remove from tracking (keep files)
dvc remove <path>.dvc

# List remotes
dvc remote list

# Update remote URL
dvc remote modify myremote url gs://new-bucket/path
```

## Summary

- **Method**: DVC (Data Version Control)
- **Justification**: Standard tool for ML/data versioning, explicitly mentioned in MS4
- **Version tracking**: `.dvc` metadata files in git, large data in GCS remote
- **Retrieval**: `dvc pull` equivalent to "dvc pull" requirement
- **Reproducibility**: Git commits + DVC metadata provide full version history
- **No LLM generation**: Uses pre-trained embeddings, no prompts/outputs to version
