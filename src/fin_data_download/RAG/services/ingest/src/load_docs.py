import os, re, glob
from typing import List, Tuple

SANITIZED_DIR = os.getenv("ARTIFACTS_DIR", "/app/artifacts") + "/sanitized"
os.makedirs(SANITIZED_DIR, exist_ok=True)

BOM = "\ufeff"
UNICODE_FIX = {
    "\u2013": "-", "\u2014": "-",
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
}
WS = re.compile(r"\s+")

def _norm(text: str) -> str:
    """Remove BOM, normalize punctuation, and collapse ALL whitespace (incl. newlines) to single spaces."""
    if not text:
        return ""
    text = text.replace(BOM, "")
    for k, v in UNICODE_FIX.items():
        text = text.replace(k, v)
    return WS.sub(" ", text).strip()

def _save_sanitized(stub: str, text: str) -> None:
    out = os.path.join(SANITIZED_DIR, stub)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)

def load_txt_md(path: str) -> List[Tuple[str, str]]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        txt = _norm(f.read())
    _save_sanitized(os.path.basename(path) + ".san.txt", txt)
    return [(path, txt)]

def load_pdf(path: str) -> List[Tuple[str, str]]:
    import fitz  # PyMuPDF
    doc = fitz.open(path)
    items: List[Tuple[str, str]] = []
    base = os.path.basename(path)
    for i, page in enumerate(doc, start=1):
        txt = _norm(page.get_text("text"))
        if not txt:
            continue
        _save_sanitized(f"{base}.page_{i:04}.txt", txt)
        items.append((f"{path}#page={i}", txt))
    return items

def load_all(data_dir: str) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for p in sorted(glob.glob(os.path.join(data_dir, "**", "*"), recursive=True)):
        if not os.path.isfile(p):
            continue
        ext = os.path.splitext(p)[1].lower()
        try:
            if ext in (".txt", ".md"):
                out.extend(load_txt_md(p))
            elif ext == ".pdf":
                out.extend(load_pdf(p))
        except Exception as e:
            print(f"[WARN] failed to read {p}: {e}")
    return out
