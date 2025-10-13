import os
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "/chroma")
VECTOR_COLLECTION = os.getenv("VECTOR_COLLECTION", "stocks_rag_v1")
DATA_DIR = os.getenv("DATA_DIR", "/app/data")
ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", "/app/artifacts")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

