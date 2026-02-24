# chunking.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class Chunk:
    chunk_id: str         # e.g., "customer_001_notes.txt::0003"
    source_file: str      # e.g., "customer_001_notes.txt"
    text: str             # the chunk text

def chunk_text(text: str, chunk_size: int = 600, overlap: int = 120) -> List[str]:
    """
    Simple sliding-window chunker.
    - chunk_size/overlap are in characters (keeps it easy + dependency-free).
    """
    text = text.strip()
    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks

def make_chunks(source_file: str, text: str, chunk_size: int = 600, overlap: int = 120) -> List[Chunk]:
    raw_chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    out: List[Chunk] = []
    for i, c in enumerate(raw_chunks):
        out.append(
            Chunk(
                chunk_id=f"{source_file}::{i:04d}",
                source_file=source_file,
                text=c.strip(),
            )
        )
    return out
