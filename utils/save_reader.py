import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(PROJECT_ROOT, "gameData")
SAVE_PATH = os.path.join(SAVE_DIR, "player_save.json")

def load_save(path=SAVE_PATH):
    # if not folder
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # if no file use default
    if not os.path.exists(path):
        print("[SAVE] No save file found, using default.")
        return default_save()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data

    except json.JSONDecodeError:
        print("[SAVE] Corrupted save file, reset to default.")
        return default_save()

def default_save():
    return {
        "player": {
            "rod": "Novice Rod",
        "default-axis": "horizontal"
        }
    }
