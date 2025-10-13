import os, time, json
from typing import List, Tuple
import chromadb
from fastembed import TextEmbedding

# Settings via env (matches your settings.py, but avoids import issues)
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "/chroma")
VECTOR_COLLECTION = os.getenv("VECTOR_COLLECTION", "stocks_rag_v1")
DATA_DIR          = os.getenv("DATA_DIR", "/app/data")
ARTIFACTS_DIR     = os.getenv("ARTIFACTS_DIR", "/app/artifacts")
CHUNK_SIZE        = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP     = int(os.getenv("CHUNK_OVERLAP", "150"))
EMBEDDING_MODEL   = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

# Import our doc loader (supports .txt/.md/.pdf with PyMuPDF)
from .load_docs import load_all

# Simple, safe chunker (independent of other modules)
def split_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    text = text or ""
    chunk_size = max(1, chunk_size)
    overlap = max(0, min(overlap, chunk_size - 1))
    chunks: List[str] = []
    i = 0
    L = len(text)
    while i < L:
        j = min(i + chunk_size, L)
        chunks.append(text[i:j])
        if j == L:
            break
        i = j - overlap
    return chunks

def main():
    t0 = time.time()
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    # 1) Load docs: returns List[(source, text)]
    docs: List[Tuple[str, str]] = load_all(DATA_DIR)
    if not docs:
        print(f"[WARN] No documents found under {DATA_DIR}")
    total_docs = len(docs)

    # 2) Chunk
    items = []  # (id, doc, meta)
    for src, txt in docs:
        chunks = split_text(txt, CHUNK_SIZE, CHUNK_OVERLAP)
        for idx, ch in enumerate(chunks):
            cid = f"{src}::chunk_{idx}"
            items.append((cid, ch, {"source": src}))

    # 3) Embed + Upsert to Chroma
    client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
    coll = client.get_or_create_collection(name=VECTOR_COLLECTION)

    # Using Chroma's server-side embedding storage (we pass only docs, not embeddings)
    # But for better compatibility with different backends we’ll explicitly create embeddings via FastEmbed.
    embedder = TextEmbedding(model_name=EMBEDDING_MODEL)

    ids, docs_list, metas = [], [], []
    for cid, ch, meta in items:
        ids.append(cid)
        docs_list.append(ch)
        metas.append(meta)

    # Batch to keep memory small
    B = 256
    added = 0
    for i in range(0, len(ids), B):
        j = i + B
        batch_ids   = ids[i:j]
        batch_docs  = docs_list[i:j]
        batch_metas = metas[i:j]

        # Compute embeddings for the batch (FastEmbed yields numpy arrays -> convert to lists)
        embs = []
        for e in embedder.passage_embed(batch_docs):
            embs.append(e.tolist() if hasattr(e, "tolist") else e)

        coll.add(ids=batch_ids, documents=batch_docs, metadatas=batch_metas, embeddings=embs)
        added += len(batch_ids)

    # 4) Write artifacts
    summary = {
        "num_input_docs": total_docs,
        "num_chunks": len(items),
        "collection": VECTOR_COLLECTION,
        "data_dir": DATA_DIR,
        "vector_store_path": VECTOR_STORE_PATH,
        "embedding_model": EMBEDDING_MODEL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "elapsed_sec": round(time.time() - t0, 2),
    }
    with open(os.path.join(ARTIFACTS_DIR, "ingest_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # Sample retrieval sanity check
    try:
        q = "What is P/E ratio?"
        q_emb = next(embedder.query_embed(q))
        if hasattr(q_emb, "tolist"):
            q_emb = q_emb.tolist()
        res = coll.query(query_embeddings=[q_emb], n_results=2, include=["documents","metadatas","distances"])
        with open(os.path.join(ARTIFACTS_DIR, "retrieval_sample.json"), "w", encoding="utf-8") as f:
            json.dump({"query": q, "results": res}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        with open(os.path.join(ARTIFACTS_DIR, "retrieval_sample.json"), "w", encoding="utf-8") as f:
            json.dump({"query": "What is P/E ratio?", "error": str(e)}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(ARTIFACTS_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump({
            "collection": VECTOR_COLLECTION,
            "num_chunks": len(items),
            "embedding_model": EMBEDDING_MODEL,
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP
        }, f, ensure_ascii=False, indent=2)

    print(f"Indexed {added} chunks into collection '{VECTOR_COLLECTION}' (FastEmbed).")

if __name__ == "__main__":
    main()
