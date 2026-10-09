import json
import os
from utils.save_reader import load_save

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(PROJECT_ROOT, "gameData")
SAVE_PATH = os.path.join(SAVE_DIR, "player_save.json")

def write_save(data, path=SAVE_PATH):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("[SAVE] Save updated at:", path)


class SaveManager:
    def __init__(self, path=SAVE_PATH):
        self.path = path
        self.data = load_save(path)

    def save(self):
        write_save(self.data, self.path)
