from __future__ import annotations
from typing import Any, Dict, List

from retrieval import retrieve_top_k

def build_context_block(results: List[Dict[str, Any]]) -> str:
    """
    Build a single context string containing retrieved chunks with citations.
    """
    blocks = []
    for r in results:
        # Use the chunk_id already formatted like "file::0003"
        citation = f"[{r['chunk_id']}]"
        blocks.append(f"{citation}\n{r['text']}".strip())
    return "\n\n---\n\n".join(blocks)

def retrieve_context(query: str, index: List[Dict[str, Any]], top_k: int = 5) -> str:
    results = retrieve_top_k(query=query, index=index, top_k=top_k)
    return build_context_block(results)
