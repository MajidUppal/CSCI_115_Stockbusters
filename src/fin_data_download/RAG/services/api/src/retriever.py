import chromadb
from fastembed import TextEmbedding
from . import settings

class Retriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_STORE_PATH)
        self.collection = self.client.get_or_create_collection(name=settings.VECTOR_COLLECTION)
        self.model = TextEmbedding(model_name=settings.EMBEDDING_MODEL)

    def stats(self):
        try:
            cnt = self.collection.count()
        except Exception:
            cnt = None
        return {"collection": settings.VECTOR_COLLECTION, "emb_model": settings.EMBEDDING_MODEL, "count": cnt}

    def _embed_query(self, q: str):
        # Try query encoder first; fallback to passage encoder
        try:
            e = next(self.model.query_embed(q))
            return e.tolist() if hasattr(e, "tolist") else e
        except Exception:
            e = next(self.model.passage_embed([q]))
            return e.tolist() if hasattr(e, "tolist") else e

    def query(self, q: str, k: int = 4):
        if not isinstance(q, str) or not q.strip():
            return []
        try:
            k = max(1, min(int(k), 50))
        except Exception:
            k = 4

        try:
            q_emb = self._embed_query(q)
        except Exception:
            return []

        try:
            res = self.collection.query(
                query_embeddings=[q_emb],
                n_results=k,
                include=["documents", "metadatas", "distances"],
            )
        except Exception:
            return []

        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]

        out = []
        for i in range(min(k, len(docs))):
            out.append({
                "rank": i + 1,
                "text": docs[i],
                "metadata": metas[i] if i < len(metas) and isinstance(metas[i], dict) else {},
                "distance": dists[i] if i < len(dists) else None,
            })
        return out
