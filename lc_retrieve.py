# lc_retrieve.py

from __future__ import annotations
from typing import List, Tuple
from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

PERSIST_DIR = "lc_chroma"
COLLECTION_NAME = "cs_copilot_docs"

def _short_source(path_str: str) -> str:
    # Chroma stores full path; keep just filename for citations
    return Path(path_str).name

def retrieve_top_k(query: str, top_k: int = 6) -> List[Tuple[str, str, float]]:
    """
    Returns list of (citation, text, score).
    citation looks like: [filename::chunk-0012]
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vs = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )

    # similarity_search_with_score returns (Document, score)
    # Note: in Chroma, lower score often means "closer" (distance), depending on settings.
    # We'll convert to a "higher is better" style by negating distance for display.
    docs_scores = vs.similarity_search_with_score(query, k=top_k)

    results: List[Tuple[str, str, float]] = []
    for doc, score in docs_scores:
        src = _short_source(doc.metadata.get("source", "unknown"))
        chunk = doc.metadata.get("chunk", "na")
        citation = f"[{src}::chunk-{int(chunk):04d}]" if str(chunk).isdigit() else f"[{src}::chunk-{chunk}]"

        # Convert distance-like score to a more intuitive "bigger is better" score
        # (Purely for display/debug; retrieval order is what matters.)
        display_score = -float(score)

        results.append((citation, doc.page_content, display_score))

    return results

def build_context_block(query: str, top_k: int = 6) -> str:
    results = retrieve_top_k(query, top_k=top_k)
    blocks = []
    for citation, text, _ in results:
        blocks.append(f"{citation}\n{text}".strip())
    return "\n\n---\n\n".join(blocks)
