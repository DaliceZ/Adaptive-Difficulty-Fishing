# interface/survey.py
import pygame
import os

from gameData.config import BG_COLOR
from utils.load_img import load_ui_image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FONT_PATH = os.path.join(ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf")

SCALE_TEXT = "(0 = Not at all, 9 = Extremely)"

def draw_text(screen, text, font, color, center_x, center_y, bg_color=None):
    text_surface = font.render(text, True, color, bg_color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)

def run_survey(screen, S, mode, remaining_survey=2):
    pygame.init()
    clock = pygame.time.Clock()

    bg_img = load_ui_image("game_bg2.png")
    bg_img = pygame.transform.scale(bg_img, (S.WIDTH, S.HEIGHT))

    font_title = pygame.font.Font(FONT_PATH, int(30 * S.scale))
    font_question = pygame.font.Font(FONT_PATH, int(22 * S.scale))
    font_scale = pygame.font.Font(FONT_PATH, int(18 * S.scale))

    base_questions = [
        "How HARD was this mode?",
        "How FUN was this mode?",
    ]

    questions = list(base_questions)
    if mode == "DDA":
        questions.extend([
            "Which mode did this feel like?",
            "Was this mode MORE FUN? (0-9)",
        ])

    answers = {}
    current_question = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Return incomplete results if the user quits
                return answers
            if event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    answer = event.key - pygame.K_0

                    # DDA Q3 accepts only 1, 2, or 3
                    is_dda_q3 = (mode == "DDA" and current_question == 2)
                    if is_dda_q3 and answer not in (1, 2, 3):
                        continue

                    answers[f"Q{current_question + 1}"] = answer
                    current_question += 1
                    if current_question >= len(questions):
                        running = False

        screen.blit(bg_img, (0, 0))

        # Draw Title
        draw_text(screen, "Post-Game Survey", font_title, (255, 255, 255), S.WIDTH // 2, S.HEIGHT * 0.2)

        if current_question < len(questions):
            # Draw current question
            draw_text(screen, questions[current_question], font_question, (200, 200, 200), S.WIDTH // 2, S.HEIGHT * 0.4)

            is_dda_q3 = (mode == "DDA" and current_question == 2)
            scale_hint = "(1 = Easy, 2 = Medium, 3 = Hard)" if is_dda_q3 else SCALE_TEXT
            draw_text(screen, scale_hint, font_scale, (170, 170, 170), S.WIDTH // 2, S.HEIGHT * 0.45)

            # Draw response boxes/prompts
            prompt = "Please press 1, 2, or 3." if is_dda_q3 else "Please press a number key (0-9) to answer."
            draw_text(screen, prompt, font_scale, (255, 255, 100), S.WIDTH // 2, S.HEIGHT * 0.6)

            if is_dda_q3:
                for i in (1, 2, 3):
                    draw_text(
                        screen,
                        str(i),
                        font_question,
                        (255, 255, 255),
                        S.WIDTH // 2 + (i - 2) * 80 * S.scale,
                        S.HEIGHT * 0.7,
                    )
            else:
                spacing = 45 * S.scale
                for i in range(0, 10):
                    draw_text(
                        screen,
                        str(i),
                        font_question,
                        (255, 255, 255),
                        int(S.WIDTH // 2 + (i - 4.5) * spacing),
                        S.HEIGHT * 0.7,
                    )
        else:
            # All questions answered
            draw_text(screen, f"Thank you! Another {remaining_survey} left" if remaining_survey > 0 else "Thank you! for surveying" , font_title, (100, 255, 100), S.WIDTH // 2, S.HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(1500) # Show "Thank you" for a moment
            running = False

        pygame.display.flip()
        clock.tick(30)

    return answers
