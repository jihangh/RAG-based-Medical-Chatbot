import pickle
from pathlib import Path

CHUNK_CACHE_DIR = Path("chunk_cache")
CHUNK_CACHE_DIR.mkdir(exist_ok=True)

def save_chunks(chunks, key):
    path = CHUNK_CACHE_DIR / f"{key}.pkl"
    with open(path, "wb") as f:
        pickle.dump(chunks, f)

def load_chunks(key):
    path = CHUNK_CACHE_DIR / f"{key}.pkl"
    if path.exists():
        with open(path, "rb") as f:
            return pickle.load(f)
    return None
