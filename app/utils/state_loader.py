import yaml
from pathlib import Path

STATE_FILE = Path("rag_state.yaml")

def load_state():
    if not STATE_FILE.exists():
        return {}
    with open(STATE_FILE, "r") as f:
        return yaml.safe_load(f) or {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        yaml.safe_dump(state, f)
