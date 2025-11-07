# Single-image: ChromaDB server + RAG app with GCS FUSE support
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    CHROMA_TELEMETRY_DISABLED=1 \
    POSTHOG_DISABLED=true \
    OMP_NUM_THREADS=1

# Install system dependencies including GCS FUSE and ChromaDB
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates wget git \
    gnupg fuse mount && \
    echo "deb http://packages.cloud.google.com/apt gcsfuse-bullseye main" | \
    tee /etc/apt/sources.list.d/gcsfuse.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key add - && \
    apt-get update && \
    apt-get install -y gcsfuse && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install ChromaDB server (CLI needed for 'chroma run' command)
# Pin version to match pyproject.toml to avoid conflicts
RUN pip install --no-cache-dir "chromadb>=1.0.0"

# (Optional) uv for fast, reproducible installs
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && ln -s /root/.local/bin/uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=/.venv
ENV PATH="/.venv/bin:${PATH}"

# All app paths will live under /workspace
WORKDIR /workspace

# Project metadata + app code
COPY pyproject.toml ./
COPY rag.py ./
COPY .env ./

# GCS service account key (optional - only copies if file exists)
# Note: Remove .dockerignore entry for gcs-key.json if you want to include it
COPY gcs-key.json* ./

# Install Python deps declared in pyproject.toml
RUN uv sync

# Bake docs into the image so you don't need -v mounts
# Everything under src/rag/data/ on the host becomes /workspace/data in the image
COPY data/ /workspace/data/

# Create ChromaDB data directory (will be mounted with GCS FUSE if GCS_BUCKET_NAME is set)
RUN mkdir -p /chroma

# Expose FastAPI port and ChromaDB port
EXPOSE 8000

# Use Python directly - rag.py handles ChromaDB server startup
ENTRYPOINT ["/.venv/bin/python", "rag.py"]


  


