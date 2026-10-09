# interface/end_screen.py
import pygame
import time
import os
import random
from gameData.config import BASE_WIDTH, BASE_HEIGHT
from utils.gadgets import Button, Switch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_end_screen_meme(screen, clock, duration=4, meme_fish=False):
    if meme_fish:
        image_path= os.path.join(BASE_DIR, "assets", "images", f"meme_fish.png")
    else :
        image_path= os.path.join(BASE_DIR, "assets", "images", f"meme{random.randint(1,5)}.png")


    end_image = pygame.image.load(image_path).convert_alpha()
    end_image = pygame.transform.scale(end_image, (BASE_WIDTH, BASE_HEIGHT))

    start_time = time.time()
    image_rect = end_image.get_rect(
        center=(BASE_WIDTH // 2, BASE_HEIGHT // 2)
    )
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))
        screen.blit(end_image, image_rect)

        pygame.display.flip()
        clock.tick(60)

ROD_IMAGES = {}
# ICON_IMAGE = None

def load_images(rod_name):
    global ROD_IMAGES

    try:
        img_path = os.path.join(
            BASE_DIR, "assets", "images", "rods", f"{rod_name}.png"
        )

        # fallback path
        fallback_path = os.path.join(
            BASE_DIR, "assets", "images", "Novice Rod.png"
        )


        if os.path.exists(img_path):
            img = pygame.image.load(img_path).convert_alpha()
            
        else:
            img = pygame.image.load(fallback_path).convert_alpha()

        img = pygame.transform.rotate(img, 110)
        ROD_IMAGES[rod_name] = img
        

    except pygame.error as e:
        print(f"[IMAGE LOAD ERROR] {rod_name}: {e}")

def load_icon_image():
    global ICON_IMAGE
    try:
        icon_path = os.path.join(BASE_DIR, "assets", "images", "fish.jpg")

        # print("BASE_DIR:", BASE_DIR)
        # print("ICON PATH:", icon_path)
        # print("EXISTS:", os.path.exists(icon_path))

        if not os.path.exists(icon_path):
            print("[ERROR]: File not found")
            ICON_IMAGE = None
            return

        raw_img = pygame.image.load(icon_path).convert_alpha()
        ICON_IMAGE = pygame.transform.scale(raw_img, (32, 32))

        print("Icon loaded successfully")
        return ICON_IMAGE

    except Exception as e:
        print("[ICON LOAD ERROR]:", e)
        return None
    
def load_ui_image(filename):
    ui_path = os.path.join(BASE_DIR, "assets", "images", "ui", filename)

    if not os.path.exists(ui_path):
        raise FileNotFoundError(f"UI image not found: {filename}")

    return pygame.image.load(ui_path).convert_alpha()

def load_tutorial(filename):
    ui_path = os.path.join(BASE_DIR, "assets", "images", "tutorial", filename)

    if not os.path.exists(ui_path):
        raise FileNotFoundError(f"UI image not found: {filename}")

    return pygame.image.load(ui_path).convert_alpha()

