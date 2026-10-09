# credits.py
import pygame
import os
from utils.gadgets import Button, Switch, Slider
from gameData.config import BG_COLOR
from utils.load_img import load_ui_image
from utils.save_writer import SaveManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

FONT_PATH = os.path.join(
    ROOT_DIR,
    "assets",
    "fonts",
    "RasterForgeRegular-JpBgm.ttf"
)

def run_credits(screen, S, settings_data):
    pygame.display.set_caption("Credits")
    clock = pygame.time.Clock()

    button_img = load_ui_image("button.png")
    rect_button_img = load_ui_image("rect_button.png")
    bg_img = load_ui_image("bg2.png")
    bg_img = pygame.transform.scale(bg_img, (S.WIDTH, S.HEIGHT))

    font_title = pygame.font.Font(FONT_PATH, int(48 * S.scale))
    font_label = pygame.font.Font(FONT_PATH, int(20 * S.scale))
    gameplay_label = pygame.font.Font(FONT_PATH, int(14 * S.scale))
    font_btn = pygame.font.Font(FONT_PATH, int(24 * S.scale))

    CENTER_X = S.WIDTH // 2
    button_width = 190 * S.scale
    button_height = 80 * S.scale

    y_pos = S.HEIGHT - 200 * S.scale
    ROW_Y_START = S.HEIGHT * 0.2

    LABEL_X = CENTER_X

    setting_btn = Button(
            rect=(
                CENTER_X - button_width // 2,
                y_pos,
                button_width,
                button_height
            ),
            text="BACK",
            font=font_btn,
            image=button_img
        )

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if setting_btn.clicked(event):
                    return "SETTINGS"
            
        screen.blit(bg_img, (0, 0))

        title = font_title.render("CREDITS", True, (51,25,0))
        screen.blit(title,
                    title.get_rect(center=(CENTER_X,
                                           S.HEIGHT * 0.12)))
        screen.blit(
            font_label.render("SoundTrack: Monplaisir - Free Music", True, (51,25,0)),
            (LABEL_X- (font_label.size(f"SoundTrack: Monplaisir - Free Music")[0] // 2), ROW_Y_START + 20 * S.scale)
        )
        screen.blit(
            font_label.render("Fish: Pufferfish - Blue Reef Aquarium", True, (51,25,0)),
            (LABEL_X- (font_label.size(f"Fish: Pufferfish - Blue Reef Aquarium")[0] // 2), ROW_Y_START + 60 * S.scale)
        )
        screen.blit(
            font_label.render("Inspired by Stardewvalley & Roblox Fisch", True, (51,25,0)),
            (LABEL_X- (font_label.size(f"Inspired by Stardewvalley & Roblox Fisch")[0] // 2), ROW_Y_START + 100 * S.scale)
        )
        
        setting_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(settings_data["FPS"])
