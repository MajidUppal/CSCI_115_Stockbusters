from fastapi import FastAPI
from pydantic import BaseModel
from .retriever import Retriever
app = FastAPI(title="AC215 MS2 RAG API")
retriever = None
class QueryReq(BaseModel):
    q: str
    k: int = 4
@app.on_event("startup")
def startup():
    global retriever
    retriever = Retriever()
@app.get("/health")
def health(): return {"status":"ok", **(retriever.stats() if retriever else {})}
@app.post("/query")
def query(req: QueryReq): return {"query": req.q, "results": retriever.query(req.q, req.k)}
