from __future__ import annotations
from pathlib import Path
from typing import List, Set

DATA_DIR = Path("data")

def list_customer_ids() -> List[str]:
    ids: Set[str] = set()
    for fp in DATA_DIR.glob("*.txt"):
        name = fp.name
        if "_" in name:
            ids.add(name.split("_", 2)[0] + "_" + name.split("_", 2)[1])  # keeps customer_001
    return sorted(ids)

def filename_belongs_to_customer(filename: str, customer_id: str) -> bool:
    return filename.startswith(customer_id + "_")
