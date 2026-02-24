# load_docs.py

from __future__ import annotations
from pathlib import Path
from typing import List
from chunking import Chunk, make_chunks

DATA_DIR = Path("data")

def load_all_text_files(data_dir: Path = DATA_DIR) -> List[Chunk]:
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir.resolve()}")

    chunks: List[Chunk] = []
    for fp in sorted(data_dir.glob("*.txt")):
        text = fp.read_text(encoding="utf-8", errors="replace")
        chunks.extend(make_chunks(source_file=fp.name, text=text))
    return chunks

if __name__ == "__main__":
    chunks = load_all_text_files()
    print(f"Loaded {len(chunks)} chunks from {DATA_DIR}/")
    # Print a quick preview
    for c in chunks[:3]:
        print("\n---")
        print(c.chunk_id)
        print(c.text[:250])
