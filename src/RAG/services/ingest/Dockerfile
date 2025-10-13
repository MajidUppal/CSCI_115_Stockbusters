FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends git curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
RUN uv sync
COPY src /app/src
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python","-m","src.build_index"]
