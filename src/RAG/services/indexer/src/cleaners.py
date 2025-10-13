import re, unicodedata
ZW = ["\u200b","\u200c","\u200d","\ufeff"]
def normalize_text(s:str)->str:
    if not s: return s
    s = unicodedata.normalize("NFKC", s)
    for z in ZW: s = s.replace(z,"")
    s = s.replace("“",'"').replace("”",'"').replace("’","'").replace("‘","'")
    s = re.sub(r"[ \t]+"," ", s)
    s = re.sub(r"\n{3,}","\n\n", s)
    return s.strip()
