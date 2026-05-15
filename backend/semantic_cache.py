from __future__ import annotations

import os
import pickle
import time
from typing import Any, Dict, List, Optional, Tuple

import faiss
import numpy as np

from .llm_setup import embeddings


CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache_store")
FAISS_INDEX_PATH = os.path.join(CACHE_DIR, "semantic_cache.index")
METADATA_PATH = os.path.join(CACHE_DIR, "metadata.pkl")

# In-memory FAISS index and metadata
_INDEX: Optional[faiss.IndexFlatL2] = None
_METADATA: List[Dict[str, Any]] = []


def _ensure_cache_dir() -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)


def _load_cache() -> None:
    global _INDEX, _METADATA
    _ensure_cache_dir()
    
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(METADATA_PATH):
        try:
            _INDEX = faiss.read_index(FAISS_INDEX_PATH)
            with open(METADATA_PATH, "rb") as fh:
                _METADATA = pickle.load(fh)
        except Exception:
            _INDEX = None
            _METADATA = []
    
    if _INDEX is None:
        # Initialize with empty index (dimension will be set on first embedding)
        _INDEX = None


def _save_cache() -> None:
    if _INDEX is not None:
        try:
            _ensure_cache_dir()
            faiss.write_index(_INDEX, FAISS_INDEX_PATH)
            with open(METADATA_PATH, "wb") as fh:
                pickle.dump(_METADATA, fh)
        except Exception:
            # best-effort persist
            pass


def query_cache(query: str, threshold: float = 0.88) -> Tuple[Optional[str], float]:
    """Return cached response and similarity if a close match is found.

    Returns (response, similarity) or (None, best_similarity).
    Uses FAISS for efficient nearest neighbor search.
    Converts L2 distance to cosine similarity.
    """
    if _INDEX is None or _INDEX.ntotal == 0:
        return None, 0.0

    emb = embeddings.embed_query(query)
    # Convert to numpy and reshape for FAISS
    emb_array = np.array([emb], dtype=np.float32)
    
    # Search for 1 nearest neighbor
    distances, indices = _INDEX.search(emb_array, k=1)
    
    if len(indices) == 0 or len(indices[0]) == 0:
        return None, 0.0
    
    # Convert L2 distance to similarity score (cosine-like)
    # L2 distance: sqrt(sum((a-b)^2))
    # For normalized vectors, this correlates with cosine distance
    l2_distance = distances[0][0]
    best_idx = indices[0][0]
    
    # Convert L2 distance to similarity (0 to 1, where 1 is identical)
    # Using: similarity = 1 / (1 + l2_distance)
    similarity = 1.0 / (1.0 + l2_distance)
    
    if best_idx < len(_METADATA) and similarity >= threshold:
        entry = _METADATA[best_idx]
        return entry.get("response"), similarity
    
    return None, similarity


def add_to_cache(query: str, response: str, meta: Optional[Dict[str, Any]] = None) -> None:
    """Add entry to FAISS-backed cache with metadata."""
    global _INDEX
    
    emb = embeddings.embed_query(query)
    emb_array = np.array([emb], dtype=np.float32)
    
    # Initialize index on first entry
    if _INDEX is None:
        dimension = len(emb)
        _INDEX = faiss.IndexFlatL2(dimension)
    
    # Add embedding to index
    _INDEX.add(emb_array)
    
    # Store metadata
    entry = {
        "query": query,
        "response": response,
        "ts": time.time(),
        "meta": meta or {},
    }
    _METADATA.append(entry)
    
    _save_cache()


def clear_cache() -> None:
    """Clear all cached entries."""
    global _INDEX, _METADATA
    _INDEX = None
    _METADATA = []
    _ensure_cache_dir()
    
    # Remove index files if they exist
    if os.path.exists(FAISS_INDEX_PATH):
        os.remove(FAISS_INDEX_PATH)
    if os.path.exists(METADATA_PATH):
        os.remove(METADATA_PATH)


def get_cache_size() -> int:
    """Return number of cached entries."""
    return _INDEX.ntotal if _INDEX is not None else 0


def get_cache_stats() -> Dict[str, Any]:
    """Return cache statistics."""
    return {
        "total_entries": get_cache_size(),
        "cache_dir": CACHE_DIR,
        "index_path": FAISS_INDEX_PATH,
        "metadata_path": METADATA_PATH,
    }


# Load existing cache on import
_load_cache()

