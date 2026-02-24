# retrieval.py

from __future__ import annotations
from typing import Any, Dict, List, Tuple
import numpy as np

from embeddings import embed_texts
from typing import Optional
from customers import filename_belongs_to_customer

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def retrieve_top_k(
    query: str,
    index: List[Dict[str, Any]],
    top_k: int = 5,
    customer_id: Optional[str] = None
) -> List[Dict[str, Any]]:

    """
    Returns top_k results sorted by similarity desc.
    Each result includes: score, chunk_id, source_file, text
    """
    query_vec = embed_texts([query])[0]
    q = np.array(query_vec, dtype=np.float32)

    results: List[Tuple[float, Dict[str, Any]]] = []

    for item in index:
        if customer_id and not filename_belongs_to_customer(item["source_file"], customer_id):
            continue
        ...
        v = np.array(item["embedding"], dtype=np.float32)
        score = cosine_similarity(q, v)
        results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)

    out: List[Dict[str, Any]] = []
    for score, item in results[:top_k]:
        out.append(
            {
                "score": round(score, 4),
                "chunk_id": item["chunk_id"],
                "source_file": item["source_file"],
                "text": item["text"],
            }
        )
    return out
