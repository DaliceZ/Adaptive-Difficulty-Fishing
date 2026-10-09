# setting.py
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

def run_settings(screen, S, settings_data):
    pygame.display.set_caption("Settings")
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
    ROW_Y_START = S.HEIGHT * 0.2
    ROW_GAP = 70 * S.scale

    LABEL_X = CENTER_X - 240 * S.scale
    CONTROL_X = CENTER_X + 20 * S.scale

    CONTROL_W = 260 * S.scale
    CONTROL_H = 45 * S.scale

    # ──────────────────────────────
    # RESOLUTION SLIDER
    # ──────────────────────────────

    resolutions = [
        (600, 800),
        (700, 900),
        (800, 1000),
        (900, 1100),
        (1000, 1200)
    ]

    res_index = resolutions.index(
        (settings_data["width"], settings_data["height"])
    )

    res_slider = Slider(
        rect=(CONTROL_X, ROW_Y_START + 20 * S.scale, CONTROL_W, 20),
        min_val=0,
        max_val=len(resolutions) - 1,
        start_val=res_index
    )

    # ──────────────────────────────
    # GAMEPLAY SWITCH
    # ──────────────────────────────

    gameplay_switch = Switch(
        rect=(CONTROL_X, ROW_Y_START + ROW_GAP, CONTROL_W, CONTROL_H),
        left_text="HORIZONTAL",
        right_text="VERTICAL",
        font=gameplay_label,
        initial=settings_data["gameplay"] == "horizontal"
    )

    # ──────────────────────────────
    # SFX SWITCH
    # ──────────────────────────────

    sfx_switch = Switch(
        rect=(CONTROL_X, ROW_Y_START + ROW_GAP * 2, CONTROL_W, CONTROL_H),
        left_text="ON",
        right_text="MUTE",
        font=font_btn,
        initial=settings_data["sfx"]
    )

    # ──────────────────────────────
    # FPS SLIDER
    # ──────────────────────────────

    display_info = pygame.display.Info()
    refresh_rate = getattr(display_info, "current_h", 60)

    # Available FPS options
    fps_options = [30, 60]

    # Only allow 120 if monitor likely supports it
    if refresh_rate >= 120:
        fps_options.append(120)

    fps_slider = Slider(
        rect=(CONTROL_X, ROW_Y_START + ROW_GAP * 3 + 20 * S.scale,
              CONTROL_W, 20),
        min_val=30,
        max_val=max(fps_options),
        start_val=settings_data["FPS"]
    )

    # ──────────────────────────────
    # NAVIGATION BUTTONS
    # ──────────────────────────────

    howto_btn = Button(
        rect=(S.WIDTH * 0.05,
            ROW_Y_START + ROW_GAP * 4,
            S.WIDTH * 0.9,
            60 * S.scale),
        text="HOW TO PLAY",
        font=font_btn,
        image=rect_button_img
    )

    credits_btn = Button(
        rect=(S.WIDTH * 0.05,
            ROW_Y_START + ROW_GAP * 4.8,
            S.WIDTH * 0.9,
            60 * S.scale),
        text="CREDITS",
        font=font_btn,
        image=rect_button_img
    )

    delete_btn = Button(
        rect=(S.WIDTH * 0.05,
            ROW_Y_START + ROW_GAP * 5.6,
            S.WIDTH * 0.9,
            60 * S.scale),
        text="DELETE GAME DATA",
        font=font_btn,
        image=rect_button_img
    )

    cancel_btn = Button(
        rect=(S.WIDTH * 0.08,
              ROW_Y_START + ROW_GAP * 7,
              200 * S.scale,
              80 * S.scale),
        text="CANCEL",
        font=font_btn,
        image=button_img
    )

    save_btn = Button(
        rect=(S.WIDTH * 0.92 - 200 * S.scale,
              ROW_Y_START + ROW_GAP * 7,
              200 * S.scale,
              80 * S.scale),
        text="SAVE",
        font=font_btn,
        image=button_img
    )

    save = SaveManager()
    running = True
    confirm_delete = False

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "QUIT"

            # Handle sliders
            res_slider.handle_event(event)
            fps_slider.handle_event(event)

            # Update Resolution from slider
            res_index = round(res_slider.value)
            w, h = resolutions[res_index]
            settings_data["width"] = w
            settings_data["height"] = h

            # Update FPS
            settings_data["FPS"] = int(fps_slider.value)

            # Gameplay
            if gameplay_switch.clicked(event):
                settings_data["gameplay"] = (
                    "horizontal" if gameplay_switch.value else "vertical"
                )

            # SFX
            if sfx_switch.clicked(event):
                settings_data["sfx"] = sfx_switch.value

            # Navigate
            if howto_btn.clicked(event):
                return "HOW_TO_PLAY"

            if credits_btn.clicked(event):
                return "CREDITS"
            
            # DELETE DATA
            if delete_btn.clicked(event):

                if not confirm_delete:
                    confirm_delete = True
                    delete_btn.text = "CLICK AGAIN TO CONFIRM"
                    delete_btn.bg_color = (200, 50, 50)
                    delete_btn.hover_color = (220, 50, 50)
                else:
                    # Reset Player Data
                    save.data["player"] = {
                        "rod": "Novice Rod",
                        "catched_fish": [],
                        "total_catched": 0,
                        "catched_streak": 0,
                        "perfect_catches": 0,
                        "unlocked_rods": ["Novice Rod"],
                        "shown_unlock_notice": ["Novice Rod"],
                        "historical_stats": {
                            "EASY": {
                                "plays": 0,
                                "wins": 0,
                                "avg_accuracy": 0.0,
                                "avg_time_taken": 0.0
                            },
                            "MEDIUM": {
                                "plays": 0,
                                "wins": 0,
                                "avg_accuracy": 0.0,
                                "avg_time_taken": 0.0
                            },
                            "HARD": {
                                "plays": 0,
                                "wins": 0,
                                "avg_accuracy": 0.0,
                                "avg_time_taken": 0.0
                            },
                            "DDA": {
                                "plays": 0,
                                "wins": 0,
                                "avg_accuracy": 0.0,
                                "avg_time_taken": 0.0
                            }
                        }
                    }

                    save.save()

                    confirm_delete = False
                    delete_btn.text = "DATA DELETED!"
                    delete_btn.bg_color = (70, 70, 70)
                    delete_btn.hover_color = (70, 70, 70)

            if cancel_btn.clicked(event):
                return "LOBBY"

            if save_btn.clicked(event):
                save.data["settings_data"] = settings_data
                save.save()

                # Apply resolution immediately
                screen = pygame.display.set_mode(
                    (settings_data["width"],
                     settings_data["height"])
                )

                return "LOBBY"

        # ──────────────────────────────
        # DRAW
        # ──────────────────────────────

        screen.blit(bg_img, (0, 0))

        title = font_title.render("SETTINGS", True, (51,25,0))
        screen.blit(title,
                    title.get_rect(center=(CENTER_X,
                                           S.HEIGHT * 0.12)))

        # Labels
        screen.blit(
            font_label.render("RESOLUTION", True, (51,25,0)),
            (LABEL_X, ROW_Y_START + 20 * S.scale)
        )

        screen.blit(
            font_label.render("GAMEPLAY", True, (51,25,0)),
            (LABEL_X, ROW_Y_START + ROW_GAP + 15 * S.scale)
        )

        screen.blit(
            font_label.render("SFX", True, (51,25,0)),
            (LABEL_X, ROW_Y_START + ROW_GAP * 2 + 15 * S.scale)
        )

        screen.blit(
            font_label.render("FPS", True, (51,25,0)),
            (LABEL_X, ROW_Y_START + ROW_GAP * 3 + 20 * S.scale)
        )
        res_index = round(res_slider.value)
        w, h = resolutions[res_index]
        # Draw sliders
        res_slider.draw(screen)
        fps_slider.draw(screen)

        # Resolution text
        res_text = font_btn.render(
            f"{w} x {h}",
            True,
            (51,25,0)
        )
        screen.blit(res_text,
                    (CONTROL_X,
                     ROW_Y_START - 5 * S.scale))

        # FPS text
        fps_text = font_btn.render(
            str(settings_data["FPS"]),
            True,
            (51,25,0)
        )
        screen.blit(fps_text,
                    (CONTROL_X,
                     ROW_Y_START + ROW_GAP * 3 - 5 * S.scale))

        # Draw switches
        gameplay_switch.draw(screen)
        sfx_switch.draw(screen)

        # Draw buttons
        howto_btn.draw(screen)
        credits_btn.draw(screen)
        delete_btn.draw(screen)


        cancel_btn.draw(screen)
        save_btn.draw(screen)

        pygame.display.flip()
        clock.tick(settings_data["FPS"])
