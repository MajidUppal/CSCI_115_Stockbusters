import os
API_PORT = int(os.getenv("API_PORT", "8000"))
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "/chroma")
VECTOR_COLLECTION = os.getenv("VECTOR_COLLECTION", "stocks_rag_v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

