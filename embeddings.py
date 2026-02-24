# embeddings.py

from __future__ import annotations
from typing import List
from ai_client import get_client

EMBEDDING_MODEL = "text-embedding-3-small"

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Create embeddings for a list of texts using OpenAI embeddings.
    Returns a list of vectors (list[float]), one per input text.
    """
    if not texts:
        return []

    client = get_client()

    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    # The API returns embeddings in the same order as inputs
    return [item.embedding for item in resp.data]


def embed_texts_batched(texts: List[str], batch_size: int = 64) -> List[List[float]]:
    """
    Same as embed_texts, but batches requests to avoid large payloads.
    """
    all_vecs: List[List[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        all_vecs.extend(embed_texts(batch))
    return all_vecs
