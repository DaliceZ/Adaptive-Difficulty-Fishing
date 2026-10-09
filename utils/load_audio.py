import pygame
import os

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Global SFX variables
stab_sfx = None
lobby_sfx = None
meme_sfx = None
meme_fish_sfx = None
unlock_sfx = None
button_sfx = None
warned_sfx = None
meme_rod_sfx = None
reeling_sfx = None
caught_sfx = None
failed_sfx = None

def load_sfx():
    global stab_sfx, lobby_sfx, meme_sfx, meme_fish_sfx, unlock_sfx, button_sfx, warned_sfx, meme_rod_sfx, reeling_sfx, caught_sfx, failed_sfx
    
    try:
        lobby_path = os.path.join(BASE_DIR, "assets", "sfx", "monplaisir.wav")
        lobby_sfx = pygame.mixer.Sound(lobby_path)
        
        stab_path = os.path.join(BASE_DIR, "assets", "sfx", "slash.wav")
        stab_sfx = pygame.mixer.Sound(stab_path)
        stab_sfx.set_volume(0.25)
        
        meme_path = os.path.join(BASE_DIR, "assets", "sfx", "meme.wav")
        meme_sfx = pygame.mixer.Sound(meme_path)
        meme_sfx.set_volume(2.0)
        
        meme_fish_path = os.path.join(BASE_DIR, "assets", "sfx", "meme_fish.wav")
        meme_fish_sfx = pygame.mixer.Sound(meme_fish_path)
        meme_fish_sfx.set_volume(1.0)

        unlock_path = os.path.join(BASE_DIR, "assets", "sfx", "unlock.wav")
        unlock_sfx = pygame.mixer.Sound(unlock_path)
        unlock_sfx.set_volume(1.0)

        button_path = os.path.join(BASE_DIR, "assets", "sfx", "button.wav")
        button_sfx = pygame.mixer.Sound(button_path)
        button_sfx.set_volume(1.0)

        warned_path = os.path.join(BASE_DIR, "assets", "sfx", "warned.wav")
        warned_sfx = pygame.mixer.Sound(warned_path)
        warned_sfx.set_volume(1.0)

        meme_rod_path = os.path.join(BASE_DIR, "assets", "sfx", "meme_effect.wav")
        meme_rod_sfx = pygame.mixer.Sound(meme_rod_path)
        meme_rod_sfx.set_volume(1.0)

        reeling_path = os.path.join(BASE_DIR, "assets", "sfx", "reeling.wav")
        reeling_sfx = pygame.mixer.Sound(reeling_path)
        reeling_sfx.set_volume(0.5)

        caught_path = os.path.join(BASE_DIR, "assets", "sfx", "caught.wav")
        caught_sfx = pygame.mixer.Sound(caught_path)
        caught_sfx.set_volume(0.5)

        failed_path = os.path.join(BASE_DIR, "assets", "sfx", "failed.wav")
        failed_sfx = pygame.mixer.Sound(failed_path)
        failed_sfx.set_volume(0.5)

    except pygame.error as e:
        print(f"Error loading sound files: {e}")

def trigger_jumpscare(meme_fish=False):
    if meme_fish and meme_fish_sfx:
        meme_fish_sfx.play()
    elif meme_sfx:
        meme_sfx.play()

def play_lobby_sfx():
    if lobby_sfx:
        pygame.mixer.init()
        lobby_sfx.play(-1)

def play_stab_sfx():
    if stab_sfx:
        stab_sfx.play()

def stop_lobby_sfx():
    if lobby_sfx:
        lobby_sfx.stop()

def play_unlock_sfx():
    if unlock_sfx:
        unlock_sfx.play()

def play_button_sfx():
    if button_sfx:
        button_sfx.play()

def play_warned_sfx():
    if warned_sfx:
        warned_sfx.play()

def play_meme_sfx():
    if meme_rod_sfx:
        pygame.mixer.init()
        meme_rod_sfx.play(-1)

def stop_meme_sfx():
    if meme_rod_sfx:
        meme_rod_sfx.stop()

def play_reeling_sfx():
    if reeling_sfx:
        pygame.mixer.init()
        reeling_sfx.play(-1)

def stop_reeling_sfx():
    if reeling_sfx:
        reeling_sfx.stop()

def play_caught_sfx():
    if caught_sfx:
        caught_sfx.play()

def play_failed_sfx():
    if failed_sfx:
        failed_sfx.play()