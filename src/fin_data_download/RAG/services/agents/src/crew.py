import os, httpx
QUESTION = os.getenv("QUESTION","Explain P/E ratio")
API = os.getenv("RAG_API","http://api:8000/query")

def ask(q):
    with httpx.Client(timeout=30.0) as c:
        r = c.post(API, json={"q": q, "k": 4})
        r.raise_for_status()
        return r.json()["results"]

def format_answer(q, hits):
    lines = [f"Q: {q}", "A (retrieved):"]
    for i,h in enumerate(hits,1):
        src = h.get("metadata",{}).get("source","?")
        lines.append(f"{i}. {h['text'][:200]} ...  (source: {src})")
    return "\n".join(lines)

if __name__ == "__main__":
    hits = ask(QUESTION)
    print(format_answer(QUESTION, hits))
