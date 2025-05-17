import json
from pathlib import Path

STATE_FILE = Path("player_state.json")
player_states = {}

def load_state():
    global player_states
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            player_states = json.load(f)

def save_state():
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(player_states, f, indent=2)

def update_state(player_id: str, key: str, value):
    if player_id not in player_states:
        player_states[player_id] = {}
    player_states[player_id][key] = value
    save_state()

def get_state(player_id: str, key: str):
    return player_states.get(player_id, {}).get(key)

def reset_state(player_id: str):
    if player_id in player_states:
        del player_states[player_id]
        save_state()
