from langchain_text_splitters import RecursiveCharacterTextSplitter
def make_splitter(size=850, overlap=150):
    return RecursiveCharacterTextSplitter(
        chunk_size=size, chunk_overlap=overlap, length_function=len,
        separators=["\n## ","\n### ","\n\n",". "," ",""]
    )
