from pathlib import Path
from functools import lru_cache
from app.utils.exceptions import PromptFileNotFoundError

# load the system prompt
def load_system_prompt(path: str = "app/resources/prompts/system_prompt.txt") -> str:
    prompt_path = Path(path)

    if not prompt_path.exists():
        raise PromptFileNotFoundError(f"System prompt file not found: {prompt_path.resolve()}")

    with prompt_path.open("r", encoding="utf-8") as f:
        return f.read()
