# lc_build_index.py
from __future__ import annotations
from pathlib import Path
from ai_client import get_client

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = Path("data")
PERSIST_DIR = "lc_chroma"
COLLECTION_NAME = "cs_copilot_docs"

def main() -> None:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Missing data dir: {DATA_DIR.resolve()}")

    # Load all .txt files in /data
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    docs = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=120,
    )
    split_docs = splitter.split_documents(docs)

    # Add richer metadata (helps for citations)
    # langchain already sets doc.metadata["source"] to file path
    for i, d in enumerate(split_docs):
        d.metadata["chunk"] = i  # simple stable index in this build run

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Build + persist vector store
    vs = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
    )
    #vs.persist() --------> Not supported in Chroma 0.4.x --- Auto Persistence

    print(f"Loaded {len(docs)} files")
    print(f"Created {len(split_docs)} chunks")
    print(f"Persisted Chroma index to: {PERSIST_DIR}/ (collection={COLLECTION_NAME})")

if __name__ == "__main__":
    main()
