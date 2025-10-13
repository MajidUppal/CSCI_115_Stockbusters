from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data"
STORAGE = ROOT / "volumes" / "chroma"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
CHUNK_SIZE = 850
CHUNK_OVERLAP = 150
ALLOWED = {".pdf", ".md", ".txt", ".html", ".htm"}

