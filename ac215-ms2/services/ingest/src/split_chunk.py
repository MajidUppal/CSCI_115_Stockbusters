from typing import List, Dict
from . import settings
def chunk_text(text, size, overlap):
    if size <= 0: return [text]
    chunks, i, n = [], 0, len(text)
    while i < n:
        j = min(i + size, n)
        chunks.append(text[i:j])
        if j == n: break
        i = j - overlap if j - overlap > i else j
    return chunks
def chunk_documents(records):
    out = []
    for r in records:
        for idx, c in enumerate(chunk_text(r["text"], settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)):
            out.append({"doc_path": r["path"], "chunk_id": f"{r['path']}::chunk_{idx}", "text": c})
    return out
if __name__ == "__main__":
    print(len(chunk_text('sample text '*50,80,20)))
