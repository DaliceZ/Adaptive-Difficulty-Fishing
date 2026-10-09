# interface/difficulty_selection.py
import pygame
import os
from gameData.config import *
from utils.load_audio import play_button_sfx
from utils.load_img import load_ui_image    

# ใช้ Font เดียวกับในเกม (อิงจาก path ใน game.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FONT_PATH = os.path.join(ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf")

def draw_text_centered(screen, text, font, color, center_x, center_y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)
    return text_rect

def run_difficulty_selection(screen, S):
    pygame.init()
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(FONT_PATH, int(30 * S.scale))
    font_btn = pygame.font.Font(FONT_PATH, int(20 * S.scale))

    bg_img = load_ui_image("bg2.png")
    bg_img = pygame.transform.scale(bg_img, (S.WIDTH, S.HEIGHT))

    running = True
    selected_difficulty = "DDA" # Default fallback

    while running:
        screen.blit(bg_img, (0, 0))
        
        # Title
        draw_text_centered(screen, "SELECT DIFFICULTY", font_title, (51, 25, 0), S.WIDTH // 2, S.HEIGHT * 0.2)

        mouse_pos = pygame.mouse.get_pos()
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        # Back button
        back_btn_rect = pygame.Rect(S.WIDTH * 0.05, S.HEIGHT * 0.05, S.WIDTH * 0.2, S.HEIGHT * 0.07)
        back_btn_rect.center = (S.WIDTH * 0.15, S.HEIGHT * 0.1)
        
        is_hover_back = back_btn_rect.collidepoint(mouse_pos)
        back_color = (200, 200, 200) if is_hover_back else (100, 100, 100)
        pygame.draw.rect(screen, (50,50,50), back_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), back_btn_rect, 2, border_radius=10)
        
        back_text_color = (255, 255, 255) if is_hover_back else (200, 200, 200)
        draw_text_centered(screen, "< BACK", font_btn, back_text_color, back_btn_rect.centerx, back_btn_rect.centery)
        
        if is_hover_back and click:
            play_button_sfx()
            return "LOBBY"

        # Difficulty Buttons
        buttons = [
            ("EASY (Speed 1.0)", "EASY", 0.4, (100, 255, 100)),
            ("MEDIUM (Speed 2.0)", "MEDIUM", 0.5, (255, 255, 100)),
            ("HARD (Speed 3.0)", "HARD", 0.6, (255, 100, 100)),
            ("ADAPTIVE (DDA)", "DDA", 0.75, (100, 200, 255))
        ]

        for label, value, y_ratio, color in buttons:
            # Simple button interaction
            btn_rect = pygame.Rect(0, 0, S.WIDTH * 0.6, S.HEIGHT * 0.08)
            btn_rect.center = (S.WIDTH // 2, S.HEIGHT * y_ratio)
            
            is_hover = btn_rect.collidepoint(mouse_pos)
            
            # Draw Button Shape
            draw_color = color if is_hover else (50, 50, 50)
            pygame.draw.rect(screen, draw_color, btn_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2, border_radius=10)
            
            # Draw Text
            text_color = (0, 0, 0) if is_hover else (200, 200, 200)
            draw_text_centered(screen, label, font_btn, text_color, btn_rect.centerx, btn_rect.centery)

            if is_hover and click:
                play_button_sfx()
                return value

        pygame.display.flip()
        clock.tick(60)

    return "DDA"