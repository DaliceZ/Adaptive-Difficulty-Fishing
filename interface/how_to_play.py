import os
import pygame
from utils.load_img import load_tutorial

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

FONT_PATH = os.path.join(
    ROOT_DIR,
    "assets",
    "fonts",
    "RasterForgeRegular-JpBgm.ttf"
)

TUTORIAL_PATH = os.path.join(
    ROOT_DIR,
    "assets",
    "images",
    "tutorial"
)

def run_how_to_play(screen, S, FPS=60):

    clock = pygame.time.Clock()

    font_title = pygame.font.Font(FONT_PATH, int(36 * S.scale))
    font_text = pygame.font.Font(FONT_PATH, int(18 * S.scale))
    font_btn = pygame.font.Font(FONT_PATH, int(22 * S.scale))

    # ---- Load tutorial images ----
    tutorial_images = [
        pygame.transform.smoothscale(
            load_tutorial("step1.png"),
            (S.WIDTH, S.HEIGHT)
        ),
        pygame.transform.smoothscale(
            load_tutorial("step2.png"),
            (S.WIDTH, S.HEIGHT)
        ),
        pygame.transform.smoothscale(
            load_tutorial("step3.png"),
            (S.WIDTH, S.HEIGHT)
        ),
        pygame.transform.smoothscale(
            load_tutorial("step4.png"),
            (S.WIDTH, S.HEIGHT)
        ),
    ]

    current_step = 0

    padding = int(80 * S.scale)
    content_top = int(120 * S.scale)
    content_height = int(S.HEIGHT * 0.6)

    content_rect = pygame.Rect(
        padding,
        content_top,
        S.WIDTH - padding * 2,
        content_height
    )

    while True:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "LOBBY"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    if current_step < len(tutorial_images) - 1:
                        current_step += 1
                    else:
                        return "LOBBY"

                if event.key == pygame.K_LEFT:
                    current_step = max(0, current_step - 1)

                if event.key == pygame.K_ESCAPE:
                    return "LOBBY"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    current_step = max(0, current_step - 1)

                if next_rect.collidepoint(event.pos):
                    if current_step < len(tutorial_images) - 1:
                        current_step += 1
                    else:
                        return "LOBBY"

        # -------- DRAW --------
        screen.fill((28, 30, 40))

        # Title
        title_surface = font_title.render("HOW TO PLAY", True, (255, 255, 255))
        screen.blit(
            title_surface,
            ((S.WIDTH - title_surface.get_width()) // 2,
             int(30 * S.scale))
        )

        # ---- Draw Image ----
        screen.blit(tutorial_images[current_step], (0, 0))

        # -------------------------------------------------
        # Navigation Group
        # -------------------------------------------------

        nav_width = content_rect.width
        nav_height = int(80 * S.scale)

        nav_rect = pygame.Rect(
            content_rect.left,
            int(S.HEIGHT * 0.80),
            nav_width,
            nav_height
        )
        # Progress Bar
        bar_width = int(nav_width * 0.5)
        bar_height = int(10 * S.scale)

        bar_x = nav_rect.centerx - bar_width // 2
        bar_y = nav_rect.top + int(10 * S.scale)

        pygame.draw.rect(screen, (224, 150, 40),
                         (bar_x, bar_y, bar_width, bar_height),
                         border_radius=6)

        progress_ratio = (current_step + 1) / len(tutorial_images)

        pygame.draw.rect(screen, (51,25,0),
                         (bar_x,
                          bar_y,
                          int(bar_width * progress_ratio),
                          bar_height),
                         border_radius=6)

        # Step Text
        step_text = font_text.render(
            f"STEP {current_step + 1} / {len(tutorial_images)}",
            True,
            (51,25,0)
        )

        step_rect = step_text.get_rect(
            midtop=(nav_rect.centerx,
                    bar_y + bar_height + int(10 * S.scale))
        )

        screen.blit(step_text, step_rect)

        # Buttons
        back_label = "< BACK"
        next_label = "FINISH" if current_step == len(tutorial_images) - 1 else "NEXT >"

        back_text = font_btn.render(back_label, True, (51,25,0))
        next_text = font_btn.render(next_label, True, (51,25,0))

        back_rect = back_text.get_rect(
            midleft=(nav_rect.left, bar_y + bar_height // 2)
        )

        next_rect = next_text.get_rect(
            midright=(nav_rect.right, bar_y + bar_height // 2)
        )

        screen.blit(back_text, back_rect)
        screen.blit(next_text, next_rect)

        pygame.display.flip()