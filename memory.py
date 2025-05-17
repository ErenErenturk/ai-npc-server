import json
from pathlib import Path

MEMORY_FILE = Path("conversation_memory.json")
conversation_memory = {}

def load_memory():
    global conversation_memory
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            conversation_memory = json.load(f)

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation_memory, f, indent=2)
