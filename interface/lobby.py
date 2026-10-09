# lobby.py
import os
import pygame

from gameData.config import BG_COLOR
from utils.gadgets import Button
from utils.load_img import load_ui_image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)


FONT_PATH = os.path.join(
    ROOT_DIR,
    "assets",
    "fonts",
    "RasterForgeRegular-JpBgm.ttf"
)



def run_lobby(screen, S, FPS=60):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Fishing Lobby")
    clock = pygame.time.Clock()

    button_img = load_ui_image("button.png")
    play_button_img = load_ui_image("play_button.png")
    quit_button_img = load_ui_image("quit_button.png")
    bg_img = load_ui_image("lobby_bg.png")
    bg_img = pygame.transform.scale(bg_img, (S.WIDTH, S.HEIGHT))

    title_font = pygame.font.Font(FONT_PATH, int(42 * S.scale))
    btn_font = pygame.font.Font(FONT_PATH, int(24 * S.scale))
    ex_btn_font = pygame.font.Font(FONT_PATH, int(21 * S.scale))

    start_x = int(S.WIDTH * 0.2)
    start_y = int(S.HEIGHT * 0.2)
    gap = int(90 * S.scale)
    btn_w = int(190 * S.scale)
    btn_h = int(85 * S.scale)
    # --- Buttons ---
    buttons = [
        ("PLAY", btn_font, "GAME"),
        ("EXPERIMENT", ex_btn_font, "EXPERIMENT"),
        ("ROD", btn_font, "SELECT_ROD"),
        ("BESTIARY", btn_font, "FISH_LOG"),
        ("SETTINGS", btn_font, "SETTINGS"),
        ("QUIT", btn_font, "QUIT"),
        ]

    ui_buttons = []

    for i, (text, font_used, action) in enumerate(buttons):
        if i == 0:
            btn = Button(
                rect=(
                    start_x*0.87,
                    start_y*0.85 + i * gap,
                    btn_w*1.2,
                    btn_h*1.2
                ),
                text=text,
                font=font_used,
                image=play_button_img
            )
        elif i == 5:
            btn = Button(
                rect=(
                    start_x,
                    start_y + i * (gap-5),
                    btn_w,
                    btn_h
                ),
                text=text,
                font=font_used,
                image=quit_button_img
            )
        else:
            btn = Button(
                rect=(
                    start_x,
                    start_y + i * (gap-5),
                    btn_w,
                    btn_h
                ),
                text=text,
                font=font_used,
                image=button_img
            )
        ui_buttons.append((btn, action))

    running = True
    while running:
        for event in pygame.event.get():
            for btn, action in ui_buttons:
                if btn.clicked(event):
                    return action

        screen.blit(bg_img, (0, 0))

        # --- Title ---
        text = "Fishing DDA"
        text_color = (51, 25, 0)
        outline_color = (255, 255, 255)
        title = title_font.render(text, True, text_color)
        outline = title_font.render(text, True, outline_color)
        title_rect = title.get_rect(
            center=(start_x + 110 * S.scale, S.HEIGHT // 2 - 300 * S.scale)
        )
        thickness = 2
        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                if dx != 0 or dy != 0:
                    screen.blit(outline, title_rect.move(dx, dy))

        screen.blit(title, title_rect)

        # --- Draw Buttons ---
        for btn, _ in ui_buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
