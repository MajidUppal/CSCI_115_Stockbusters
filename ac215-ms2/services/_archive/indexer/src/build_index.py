from pathlib import Path
from bs4 import BeautifulSoup
from pypdf import PdfReader
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from cleaners import normalize_text
from splitters import make_splitter
from settings import DATA_RAW, STORAGE, EMBED_MODEL, ALLOWED

def load_file(fp: Path):
    ext = fp.suffix.lower()
    docs = []
    if ext == ".pdf":
        reader = PdfReader(str(fp))
        for i, p in enumerate(reader.pages):
            txt = normalize_text(p.extract_text() or "")
            if txt:
                docs.append(Document(page_content=txt, metadata={"source":fp.name,"path":str(fp),"page":i+1}))
    elif ext in {".md",".txt"}:
        txt = normalize_text(fp.read_text(encoding="utf-8", errors="ignore"))
        if txt:
            docs.append(Document(page_content=txt, metadata={"source":fp.name,"path":str(fp)}))
    elif ext in {".html",".htm"}:
        raw = fp.read_text(encoding="utf-8", errors="ignore")
        txt = normalize_text(BeautifulSoup(raw, "html.parser").get_text(" "))
        if txt:
            docs.append(Document(page_content=txt, metadata={"source":fp.name,"path":str(fp)}))
    return docs

def main():
    print(f"[indexer] scanning {DATA_RAW}")
    files = [f for f in DATA_RAW.rglob("*") if f.is_file() and f.suffix.lower() in ALLOWED]
    all_docs = []
    for f in files:
        all_docs.extend(load_file(f))
    print(f"[indexer] loaded raw docs: {len(all_docs)}")

    splitter = make_splitter()
    chunks = splitter.split_documents(all_docs)
    print(f"[indexer] split into chunks: {len(chunks)}")

    STORAGE.mkdir(parents=True, exist_ok=True)
    embed = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    db = Chroma.from_documents(chunks, embed, persist_directory=str(STORAGE), collection_name="stocks_rag_v1")
    db.persist()
    print(f"[indexer] persisted Chroma at {STORAGE}")

if __name__ == "__main__":
    main()

