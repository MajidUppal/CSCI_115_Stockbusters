FROM python:3.11-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"
COPY services/indexer/pyproject.toml ./pyproject.toml
RUN uv sync --frozen
COPY services/indexer/src ./src
CMD ["uv","run","python","src/build_index.py"]
