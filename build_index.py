# build_index.py

from __future__ import annotations
from typing import Dict, List, Any

from load_docs import load_all_text_files
from embeddings import embed_texts_batched
from index_store import load_index, save_index, _hash_texts

def build_in_memory_index(force_rebuild: bool = False) -> List[Dict[str, Any]]:
    chunks = load_all_text_files()
    texts = [c.text for c in chunks]
    current_hash = _hash_texts(texts)

    cached = load_index()
    if (not force_rebuild) and cached and cached.get("chunk_text_hash") == current_hash:
        return cached["index"]

    vectors = embed_texts_batched(texts, batch_size=64)
    if len(vectors) != len(chunks):
        raise RuntimeError(f"Embedding count mismatch: {len(vectors)} vs {len(chunks)}")

    index: List[Dict[str, Any]] = []
    for c, v in zip(chunks, vectors):
        index.append(
            {
                "chunk_id": c.chunk_id,
                "source_file": c.source_file,
                "text": c.text,
                "embedding": v,
            }
        )

    save_index(index=index, chunk_text_hash=current_hash)
    return index

if __name__ == "__main__":
    index = build_in_memory_index()
    print(f"Index ready with {len(index)} embedded chunks.")
    first = index[0]
    print("\nFirst item preview:")
    print("chunk_id:", first["chunk_id"])
    print("source_file:", first["source_file"])
    print("text preview:", first["text"][:180])
    print("embedding dims:", len(first["embedding"]))
