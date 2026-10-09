import json
import random
from pathlib import Path
from utils.save_writer import SaveManager

def get_fish_data():
    fish_data = {}
    path = Path(__file__).parent / "fish_data.json"
    with open(path, 'r', encoding='utf-8') as f:
        fish_data = json.load(f)
    return fish_data

def get_locked_fish_info():
    locked_info = {}
    path = Path(__file__).parent / "locked_fish_data.json"
    with open(path, 'r', encoding='utf-8') as f:
        locked_info = json.load(f)  
    return locked_info

def get_fish(rarity):
    fish_data = get_fish_data()
    return random.choice(fish_data[rarity])

def get_random_rarity(rod_name):
    rod = get_fishing_rod_info(rod_name)
    rarities = ["Common", "Uncommon", "Rare", "Legendary", "Mythical", "Meme"]
    weights = [1/2, 1/4, 1/8, 1/16, 1/32, 1/40]  # base weights

    luck = rod.get("LUCK", 0)
    if luck!=0:
        if luck < 0:
            weights[0] *= (1+abs(luck)) # common
        else :
            weights[0] *= (abs(luck)/2) # common
        weights[1] *= (1+luck) # uncommon
        weights[2] *= (1+(luck*2)) # rare
        weights[3] *= (1+(luck*4)) # legendary
        weights[4] *= (1+(luck*8)) # mythical
           
    
    result = random.choices(rarities, weights=weights, k=1)
    # print(weights)
    return result[0]

def get_fishing_rod_info(name):
    rod_data = {}
    path = Path(__file__).parent / "fishing_rod_data.json"
    with open(path, 'r', encoding='utf-8') as f:
        rod_data = json.load(f)

    return rod_data[name]

def get_rod_des():
    rod_data = {}
    path = Path(__file__).parent / "fishing_rod_data.json"
    with open(path, 'r', encoding='utf-8') as f:
        rod_data = json.load(f)

    return rod_data

def get_unlocked_rods():
    save_data = SaveManager()
    player_data = save_data.data["player"]
    if "Cool Rod" not in player_data["unlocked_rods"] and player_data["total_catched"] >= 5:
        save_data.data["player"]["unlocked_rods"].append("Cool Rod")
        save_data.save()
    if "RU Sure Rod" not in player_data["unlocked_rods"] and player_data["catched_streak"] >= 10:
        save_data.data["player"]["unlocked_rods"].append("RU Sure Rod")
        save_data.save()

    if "Shear Rod" not in player_data["unlocked_rods"] and player_data["total_catched"] >= 45:
        save_data.data["player"]["unlocked_rods"].append("Shear Rod")
        save_data.save()

    if "Anchor Rod" not in player_data["unlocked_rods"] and player_data["perfect_catches"] >= 5:
            save_data.data["player"]["unlocked_rods"].append("Anchor Rod")
            save_data.save()

    if "Prismatic Rod" not in player_data["unlocked_rods"] and all_caught_fish_legendary():
        save_data.data["player"]["unlocked_rods"].append("Prismatic Rod")
        save_data.save()
    
    if "Rod of the Conqueror" not in player_data["unlocked_rods"] and len(player_data["catched_fish"]) == (len(get_fish_data()["Common"]) 
        + len(get_fish_data()["Uncommon"]) + len(get_fish_data()["Rare"]) + len(get_fish_data()["Legendary"]) + len(get_fish_data()["Mythical"]) + len(get_fish_data()["Meme"])):
        save_data.data["player"]["unlocked_rods"].append("Rod of the Conqueror")
        save_data.save()

    if "Meme Rod" not in player_data["unlocked_rods"] and "Meme Fish" in player_data["catched_fish"]:
        save_data.data["player"]["unlocked_rods"].append("Meme Rod")
        save_data.save()

def get_locked_rod_info():
    locked_info = {}
    path = Path(__file__).parent / "locked_rod_data.json"
    with open(path, 'r', encoding='utf-8') as f:
        locked_info = json.load(f)
    return locked_info

def all_caught_fish_legendary():
    save_data = SaveManager()
    caught_fish = save_data.data["player"].get("catched_fish", [])

    fish_data = get_fish_data()
    count = 0
    for fish in fish_data["Legendary"]:
        if fish["name"] in caught_fish:
            count += 1

    return count == len(fish_data["Legendary"])