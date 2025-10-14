# Single-image setup for ingest + serve (rag.py)
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Minimal OS deps (add others only if you really need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates wget && \
    rm -rf /var/lib/apt/lists/*

# We'll run from /workspace (mounted by docker-compose)
WORKDIR /workspace

# ---- Install Python deps ----

RUN pip install --upgrade pip && pip install --no-cache-dir \
    fastapi>=0.111 \
    "uvicorn[standard]>=0.30" \
    "chromadb==0.5.5" \
    fastembed>=0.3.4 \
    onnxruntime>=1.18.0 \
    pymupdf>=1.24.0 \
    orjson>=3.10.0

# Copy the repo (lets you build without bind-mounts if desired)
COPY . /workspace

# Default entry: the single CLI file
ENTRYPOINT ["python", "rag.py"]
CMD ["--help"]




