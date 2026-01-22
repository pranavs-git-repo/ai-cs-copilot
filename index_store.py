# index_store.py

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List
import json
import hashlib

INDEX_PATH = Path("artifacts/index.json")

def _hash_texts(texts: List[str]) -> str:
    """
    Create a stable hash of the chunk texts to detect changes in source data.
    """
    h = hashlib.sha256()
    for t in texts:
        h.update(t.encode("utf-8", errors="replace"))
        h.update(b"\n---\n")
    return h.hexdigest()

def save_index(index: List[Dict[str, Any]], chunk_text_hash: str) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "chunk_text_hash": chunk_text_hash,
        "index": index,
    }
    INDEX_PATH.write_text(json.dumps(payload), encoding="utf-8")

def load_index() -> Dict[str, Any] | None:
    if not INDEX_PATH.exists():
        return None
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
