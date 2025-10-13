from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from settings import STORAGE, EMBED_MODEL, TOP_K

app = FastAPI()

class Q(BaseModel):
    q: str

# Initialize embedding + retriever
_emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
_db  = Chroma(embedding_function=_emb, persist_directory=str(STORAGE), collection_name="ms2_rag")
_retriever = _db.as_retriever(search_kwargs={"k": TOP_K})

def format_docs(docs):
    out = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        pg  = d.metadata.get("page")
        tag = f"{src}:{pg}" if pg else src
        out.append(f"[{tag}] {d.page_content}")
    return "\n\n".join(out)

@app.post("/ask")
def ask(payload: Q):
    docs = _retriever.get_relevant_documents(payload.q)
    if not docs:
        return {"answer": "No relevant context found."}
    context = format_docs(docs)
    return {
        "answer": f"(Open-source mode — no LLM)\n\nTop retrieved context:\n\n{context[:1200]}"
    }
