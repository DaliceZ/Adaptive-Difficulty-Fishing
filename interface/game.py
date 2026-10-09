# interface/game.py
import pygame
import math
import random
import time
import os
import numpy as np  # <--- เพิ่มบรรทัดนี้เข้าไปครับ
from gameData.config import *
from dda import DDAManager, update_fish_speed
from gameData.get_info import get_fish, get_fishing_rod_info, get_random_rarity
from utils.load_img import *
from utils.load_audio import play_caught_sfx, play_failed_sfx, trigger_jumpscare, play_stab_sfx, stop_meme_sfx, play_meme_sfx, play_reeling_sfx, stop_reeling_sfx
from utils.save_writer import SaveManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

FONT_PATH = os.path.join(
    ROOT_DIR,
    "assets",
    "fonts",
    "RasterForgeRegular-JpBgm.ttf"
)

def run_game(screen, S, rod_name, FPS=60, difficulty_mode="DDA", is_experiment=False):
    pygame.init()

    if rod_name == "Meme Rod":
        play_meme_sfx()

    # Create font
    try:
        font = pygame.font.Font(FONT_PATH, int(18 * S.scale))
    except:
        font = pygame.font.SysFont("arial", int(18 * S.scale))

    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption(f"DDA Experiment - Mode: {difficulty_mode}")
    clock = pygame.time.Clock()

    btn_font = pygame.font.Font(FONT_PATH, int(24 * S.scale))
    button_img = load_ui_image("button.png")

    bg_img = load_ui_image("game_bg.png")
    bg_img = pygame.transform.scale(bg_img, (S.WIDTH, S.HEIGHT))
    bg_img2 = load_ui_image("game_bg2.png")
    bg_img2 = pygame.transform.scale(bg_img2, (S.WIDTH, S.HEIGHT))

    fish_img = load_ui_image("fish.png")
    fish_img = pygame.transform.scale(
            fish_img,
            (50 * S.scale, 45 * S.scale)
        )
    fish_img2 = load_ui_image("fish2.png")
    fish_img2 = pygame.transform.scale(
            fish_img2,
            (50 * S.scale, 45 * S.scale)
        )

    button_width = 190 * S.scale
    button_height = 80 * S.scale
    button_gap = 40 * S.scale

    total_width = button_width * 2 + button_gap
    start_x = S.WIDTH // 2 - total_width // 2
    y_pos = S.HEIGHT - 200 * S.scale

    # LOAD SAVE DATA
    save = SaveManager()
    CATCHED_STREAK = save.data["player"]["catched_streak"]

    # ROD INFO
    rod_using = get_fishing_rod_info(rod_name)

    player_bar_width = S.BAR_WIDTH + (rod_using["CONTROLLED"] * S.BAR_WIDTH)
    bar_x = S.TRACK_X + S.TRACK_WIDTH // 2 - player_bar_width // 2
    bar_y = S.TRACK_Y

    EXTRA_HEIGHT = 10
    fish_height = S.BAR_HEIGHT + EXTRA_HEIGHT
    fish_y_draw = S.TRACK_Y - EXTRA_HEIGHT // 2

    encounter_start_time = time.time()

    # --- Difficulty Setup ---
    fish_speed = 1.0
    if difficulty_mode == "EASY":
        fish_speed = 1.0
    elif difficulty_mode == "MEDIUM":
        fish_speed = 2.0
    elif difficulty_mode == "HARD":
        fish_speed = 3.0

    progress = 0
    progress_bar_color = PROGRESS_BAR_COLOR

    # Fish Info
    fish_encounter = get_fish(get_random_rarity(rod_using["name"]))
    fish_resilience = fish_encounter["FISH_RESILIENCE"] + rod_using["RESILIENCE"]
    fish_progress = fish_encounter["PROGRESS_SPD"] + rod_using["PROGRESS_SPD"]

    # If Experiment, fix type of fish to "Uncommon" and use static resilience/progress for better comparison, while still applying rod modifiers
    if is_experiment:
        fish_encounter = get_fish("Uncommon")
        fish_resilience = 0.75
        fish_progress = 0

    # --- DDA MANAGER SETUP ---
    dda_manager = None
    baseline_skill = None  # <--- [เพิ่มบรรทัดนี้] เผื่อโหมดอื่นที่ไม่มี DDA จะได้ส่งค่า None ออกไปได้
    if difficulty_mode == "DDA":
        baseline_skill = 0.5

        # ดึงประวัติมาคำนวณความเก่ง
        hist_stats = save.data["player"].get("historical_stats", None)
        if hist_stats:
            if hist_stats["HARD"]["plays"] > 0 and hist_stats["HARD"]["avg_accuracy"] > 0.4:
                baseline_skill = hist_stats["HARD"]["avg_accuracy"] + 0.2
            elif hist_stats["MEDIUM"]["plays"] > 0:
                baseline_skill = hist_stats["MEDIUM"]["avg_accuracy"]
            elif hist_stats["EASY"]["plays"] > 0:
                baseline_skill = hist_stats["EASY"]["avg_accuracy"] - 0.1
            baseline_skill = np.clip(baseline_skill, 0.1, 0.9)

        dda_manager = DDAManager(
            fish_resilience=fish_resilience,
            fish_progress=fish_progress,
            baseline_skill=baseline_skill # ส่งค่าความเก่งเข้าไป
        )

        # ปรับความเร็วเริ่มต้นของปลาตามฝีมือ
        fish_speed = np.interp(baseline_skill, [0, 1], [0.8, 2.5])

    # Rod Logics
    progress_addition = 0
    conqueror_active = False
    if rod_using["name"] == "Rod of the Conqueror":
        conqueror_active = True
        progress_addition = 0.26
        progress_bar_color = (255, 215, 0)
        mult = 0.5
        fill_colors = 0

    if rod_using["name"] == "Shear Rod":
        knife_fill_remaining = 0.0
        KNIFE_FILL_TOTAL = 0.05
        KNIFE_FILL_SPEED = 0.075
        knife_checked = False
        mult = 0.5

    knife_active = False

    if rod_using["name"] == "Anchor Rod":
        is_anchor_active = True
        player_bar_width_before = S.BAR_WIDTH + (rod_using["CONTROLLED"] * S.BAR_WIDTH)

    choices = []
    if rod_using["name"] == "Meme Rod":
        choices = random.choices([1, 2, 3])
        if 1 in choices:
            fish_progress = -0.9

    # Fish Init
    fish_x = (S.TRACK_X + S.TRACK_WIDTH // 2 ) - (S.FISH_SIZE // 2)
    fish_direction = random.choice([-1, 1])

    if difficulty_mode == "DDA":
        fish_speed = random.uniform(FISH_MIN_SPEED, FISH_MAX_SPEED)

    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
    fish_target_x = fish_x

    fish_waiting = True
    resilient_timer = 0.0

    bar_velocity = 0.0
    bar_force = 0.0
    bar_bounced_left = False
    bar_bounced_right = False
    BAR_BOUNCE_DAMP = 0.5

    success = [False, "None", "None"]
    is_perfect_catch = True
    running = True
    actual_gain = 0.0

    # --- เพิ่ม 2 บรรทัดนี้ ---
    total_active_frames = 0
    total_catching_frames = 0

    play_reeling_sfx()

    while running:
        dt = clock.tick(FPS) / 1000.0
        frame_scale = dt * 60.0   # normalize to 60 FPS feel

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = time.time()
        freeze_active = (current_time - encounter_start_time) < ENCOUNTER_FREEZE_TIME

        if freeze_active and progress < (PROGRESS_INIT + progress_addition):
            progress += PROGRESS_FILL_ANIM_SPEED
            progress = min(progress, PROGRESS_INIT + progress_addition)

        # --- Player Control ---
        if not freeze_active:
            if rod_using["name"] == "Rod of the Conqueror":
                progress_bar_color = PROGRESS_BAR_COLOR
                conqueror_active = False
            if rod_using["name"] == "Meme Rod" :
                if 1 in choices and player_bar_width <= S.TRACK_WIDTH and fish_encounter["name"] != "Meme Fish":
                    player_bar_width += player_bar_width * 0.005
            if rod_using["name"] == "Anchor Rod" and is_anchor_active:
                if is_catching:
                    if player_bar_width > player_bar_width_before*0.6:
                        player_bar_width -= 0.25
                    fish_progress += 0.0003
                else:
                    is_anchor_active = False
                    fish_progress = fish_encounter["PROGRESS_SPD"]+rod_using["PROGRESS_SPD"]
                    player_bar_width = player_bar_width_before
            if fish_encounter["name"] == "Meme Fish" and player_bar_width >= 0 and rod_using["name"] != "Meme Rod":
                player_bar_width -= 0.25

            mouse_pressed = pygame.mouse.get_pressed()[0]
            if mouse_pressed:
                bar_force += BAR_FORCE_INC
            else:
                bar_force -= BAR_FORCE_DEC

            bar_force = max(0.0, min(BAR_FORCE_MAX, bar_force))
            bar_velocity = (bar_velocity + BAR_DRIFT_LEFT + bar_force) * BAR_FRICTION
            bar_velocity = max(-BAR_MAX_SPEED, min(BAR_MAX_SPEED, bar_velocity))
            bar_x += bar_velocity * frame_scale

            if bar_x <= S.BAR_MIN_X:
                bar_x = S.BAR_MIN_X
                if not bar_bounced_left:
                    bar_velocity = -bar_velocity * BAR_BOUNCE_DAMP
                    bar_bounced_left = True
                else:
                    bar_velocity = max(bar_velocity, 0)
            elif bar_x + player_bar_width >= S.BAR_MAX_X + S.BAR_WIDTH:
                bar_x = S.BAR_MAX_X + S.BAR_WIDTH - player_bar_width
                if not bar_bounced_right:
                    bar_velocity = -bar_velocity * BAR_BOUNCE_DAMP
                    bar_bounced_right = True
                else:
                    bar_velocity = min(bar_velocity, 0)
            else:
                bar_bounced_left = False
                bar_bounced_right = False

        # --- FISH MOVEMENT (CHAOS EDITION) ---
        if not freeze_active:
            if fish_waiting:
                resilient_timer += dt
                if rod_using["name"] == "Shear Rod" and not knife_active and not knife_checked:
                    if random.random() < 0.25:
                        play_stab_sfx()
                        mult = 0.5
                        knife_active = True
                        knife_checked = True
                        knife_fill_remaining = KNIFE_FILL_TOTAL
                        resilient_timer = 0
                        fish_waiting = True

                # In DDA mode, get resilience from the manager, otherwise use the static value
                current_resilience = dda_manager.get_modified_resilience() if dda_manager else fish_resilience

                if resilient_timer >= current_resilience:
                    resilient_timer = 0
                    fish_waiting = False
                    fish_direction = random.choice([-1, 1])

                    # Speed is now handled continuously by the DDA manager, so no special recalculation here.

                    distance = random.randint(FISH_MOVE_MIN_DIST, FISH_MOVE_MAX_DIST)
                    fish_target_x = fish_x + fish_direction * distance
                    fish_target_x = max(
                        S.BAR_MIN_X + (S.FISH_SIZE+10),
                        min(S.BAR_MAX_X + S.BAR_WIDTH - (S.FISH_SIZE+10), fish_target_x)
                    )
            else:
                if not knife_active:
                    # >>>>>>>>>>>> CHAOS LOGIC START <<<<<<<<<<<<
                    if difficulty_mode in ["DDA", "HARD", "MEDIUM"]:
                        if dda_manager:
                            chaos_chance = dda_manager.get_chaos_chance()
                        else: # Fallback to original logic for non-DDA modes
                            chaos_chance = 0.02 if difficulty_mode in ["DDA", "HARD"] else 0.01

                        if random.random() < chaos_chance:
                            # 40% chance to stop, 60% chance to juke
                            if random.random() < 0.4:
                                fish_waiting = True
                                resilient_timer = 0
                            else: # Juke!
                                fish_direction *= -1
                                distance = random.randint(50, 150) # Short, sharp movement
                                fish_target_x = fish_x + fish_direction * distance
                                fish_target_x = max(S.BAR_MIN_X + (S.FISH_SIZE+10), min(S.BAR_MAX_X + S.BAR_WIDTH - (S.FISH_SIZE+10), fish_target_x))
                                # Small speed burst on juke
                                fish_speed = min(3.5, fish_speed * 1.3)
                    # >>>>>>>>>>>> CHAOS LOGIC END <<<<<<<<<<<<

                    fish_x += fish_direction * fish_speed * frame_scale
                    if rod_name == "Meme Rod" and 2 in choices:
                        fish_y_draw += fish_direction * fish_speed
                        S.TRACK_Y += fish_direction * fish_speed
                        S.TRACK_X += fish_direction * fish_speed
                        bar_y += fish_direction * fish_speed

                    if ((fish_direction == 1 and fish_x >= fish_target_x) or
                        (fish_direction == -1 and fish_x <= fish_target_x)):
                        fish_x = fish_target_x
                        fish_waiting = True
                        knife_checked = False

                    if fish_x <= S.BAR_MIN_X + (S.FISH_SIZE+10):
                        fish_x = S.BAR_MIN_X + (S.FISH_SIZE+10)
                        fish_direction = 1
                        fish_waiting = True
                        knife_checked = False
                    elif fish_x >= S.BAR_MAX_X + S.BAR_WIDTH - (S.FISH_SIZE+10):
                        fish_x = S.BAR_MAX_X + S.BAR_WIDTH - (S.FISH_SIZE+10)
                        fish_direction = -1
                        fish_waiting = True
                        knife_checked = False

        # --- Collision Check ---
        fish_center = fish_x + S.FISH_SIZE / 2
        is_catching = bar_x <= fish_center <= bar_x + player_bar_width

        if knife_active:
            progress_bar_color = (255, 215, 0)
            if knife_fill_remaining == KNIFE_FILL_TOTAL:
                play_stab_sfx()
            # k_dt = clock.get_time() / 1000
            fill_amount = KNIFE_FILL_SPEED * dt
            actual_fill = min(fill_amount, knife_fill_remaining)
            knife_fill_remaining -= actual_fill
            progress += actual_fill
            if knife_fill_remaining <= 0:
                knife_active = False
                progress_bar_color = PROGRESS_BAR_COLOR

        # --- Progression Logic (Fixed) ---
        if not freeze_active:
            total_active_frames += 1 # นับเฟรมทั้งหมดที่เล่น
            if is_catching:
                total_catching_frames += 1 # นับเฟรมที่กรอบตรงกับปลา

                base_gain = PROGRESS_UP_RATE

                # Use DDA-modified progress rate if available
                current_fish_progress = dda_manager.get_modified_progress() if dda_manager else fish_progress

                raw_gain = base_gain * (1.0 + current_fish_progress)
                actual_gain = max(base_gain * 0.1, raw_gain) # Min gain guarantee
                progress += actual_gain * frame_scale
            else:
                progress -= PROGRESS_DOWN_RATE
                is_perfect_catch = False
                actual_gain = -(PROGRESS_DOWN_RATE * frame_scale)

        progress = max(0.0, min(1.0, progress))

        if progress >= 1.0:
            running = False
            success[0] = True
            success[1] = fish_encounter["rarity"]
            success[2] = fish_encounter["name"]
        elif progress <= 0:
            running = False

        # --- DDA UPDATES ---
        if dda_manager:
            dda_manager.update(is_catching)
            fish_speed = dda_manager.adjust_fish_speed(fish_speed, is_catching)
        else:
            # Legacy speed update for non-DDA modes
            fish_speed = update_fish_speed(is_catching, fish_speed)



        # --- Render ---
        screen.blit(bg_img, (0, 0))
        pygame.draw.rect(screen, TRACK_COLOR, (S.TRACK_X, S.TRACK_Y + 5 * S.scale, S.TRACK_WIDTH, S.TRACK_HEIGHT - 10 * S.scale))

        bar_draw_color = (255, 210, 85) if is_catching else BAR_COLOR
        rect = pygame.Rect(bar_x, bar_y, player_bar_width, S.BAR_HEIGHT)
        radius = int(3 * S.scale)
        aplha_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        if is_catching:
            pygame.draw.rect(aplha_surf, (*bar_draw_color, 255), (0, 0, rect.width, rect.height), border_radius=radius)
            screen.blit(aplha_surf, rect.topleft)
            pygame.draw.rect(screen, (255, 188, 0), rect, width=int(3 * S.scale), border_radius=radius)
        else:
            pygame.draw.rect(aplha_surf, (*bar_draw_color, 220), (0, 0, rect.width, rect.height), border_radius=radius)
            screen.blit(aplha_surf, rect.topleft)

        # Outer frame (dark)

        pygame.draw.rect(screen, FISH_COLOR, (fish_x, fish_y_draw, S.FISH_SIZE, fish_height), border_radius=3)

        fish_rect = fish_img.get_rect(
            center=(fish_x + S.FISH_SIZE // 2,
                    fish_y_draw + fish_height // 2 - 55 * S.scale)
        )

        screen.blit(fish_img, fish_rect)

        if rod_using["name"] == "Prismatic Rod":
            if pygame.time.get_ticks() % 1000 < 800 :
                fish_rect2 = fish_img2.get_rect(
                    center=(fish_target_x + S.FISH_SIZE // 2,
                            fish_y_draw + fish_height // 2 - 55 * S.scale)
                )
                screen.blit(fish_img2, fish_rect2)
                # pygame.draw.rect(screen, (255, 255, 255), (fish_target_x, bar_y + (S.TRACK_HEIGHT//2) - S.FISH_SIZE, S.FISH_SIZE, S.FISH_SIZE))

        if knife_active or conqueror_active:
            if conqueror_active:
                mult += 0.1
                knife_length = int(S.FISH_SIZE * (mult))
                knife_thickness = int(S.HEIGHT*2)
                angle = 0
                fill_colors = min(fill_colors + 1, 255)
            else:
                mult += 0.1
                knife_length = int(S.FISH_SIZE//mult)
                knife_thickness = int(S.HEIGHT*(2-mult if (2-mult)>=0 else 0))
                angle = 0

            knife_surf = pygame.Surface((knife_length, knife_thickness), pygame.SRCALPHA)
            if rod_using["name"] == "Shear Rod":
                knife_surf.fill(progress_bar_color)
            else:
                knife_surf.fill((255, 215, fill_colors))
            knife_rotated = pygame.transform.rotate(knife_surf, angle)
            fish_y = bar_y + (S.FISH_SIZE * S.scale)
            fish_center_x = fish_x + (S.FISH_SIZE // 2)
            fish_center_y = fish_y + (S.FISH_SIZE // 2)
            knife_rect = knife_rotated.get_rect(center=(fish_center_x, fish_center_y))
            screen.blit(knife_rotated, knife_rect)

        pygame.draw.rect(screen, (80, 80, 80), (S.WIDTH // 2 - S.PROGRESS_BAR_WIDTH // 2, S.PROGRESS_BAR_Y, S.PROGRESS_BAR_WIDTH, S.PROGRESS_BAR_HEIGHT))
        pygame.draw.rect(screen, progress_bar_color, (S.WIDTH // 2 - S.PROGRESS_BAR_WIDTH // 2, S.PROGRESS_BAR_Y, int(S.PROGRESS_BAR_WIDTH * progress), S.PROGRESS_BAR_HEIGHT))

        info_text = f"Mode:{difficulty_mode} | Speed:{fish_speed:.2f} | Catching:{is_catching}"
        gain_text = f"Gain Rate: {actual_gain:.5f} | Catched Streaks: {CATCHED_STREAK:.0f}"
        screen.blit(font.render(info_text, True, (200, 200, 200)), (10, 10))
        screen.blit(font.render(gain_text, True, (255, 255, 0)), (10, 35))

        if fish_progress != 0:
            color = (0, 255, 0) if fish_progress > 0 else (255, 80, 80)

            text_surface = font.render(
                f"Progression Speed {(fish_progress)*100:+.0f}%",
                True,
                color
            )

            text_rect = text_surface.get_rect(
                center=(
                    S.WIDTH // 2,
                    S.PROGRESS_BAR_Y + S.PROGRESS_BAR_HEIGHT + 15
                )
            )

            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        # clock.tick(FPS)



    # --- Result Screen ---
    catch_duration = time.time() - encounter_start_time

    # ------------------ แทรกระบบเก็บสถิติที่นี่ ------------------
    match_accuracy = total_catching_frames / max(1, total_active_frames)

    # เพิ่ม "DDA" เข้าไปในลิสต์
    if difficulty_mode in ["EASY", "MEDIUM", "HARD", "DDA"]:

        # 1. ถ้ายังไม่มี historical_stats เลย ให้สร้างโครงสร้างเริ่มต้น (เพิ่ม DDA เข้าไปแล้ว)
        if "historical_stats" not in save.data["player"]:
            save.data["player"]["historical_stats"] = {
                "EASY": {"plays": 0, "wins": 0, "avg_accuracy": 0.0, "avg_time_taken": 0.0},
                "MEDIUM": {"plays": 0, "wins": 0, "avg_accuracy": 0.0, "avg_time_taken": 0.0},
                "HARD": {"plays": 0, "wins": 0, "avg_accuracy": 0.0, "avg_time_taken": 0.0},
                "DDA": {"plays": 0, "wins": 0, "avg_accuracy": 0.0, "avg_time_taken": 0.0}
            }

        # 2. กันเหนียว: ถ้าไฟล์เซฟมี historical_stats แล้ว แต่ดันไม่มีโหมดที่กำลังเล่นอยู่ (เช่น ไฟล์เซฟเก่าที่ยังไม่มีคีย์ DDA)
        if difficulty_mode not in save.data["player"]["historical_stats"]:
            save.data["player"]["historical_stats"][difficulty_mode] = {
                "plays": 0, "wins": 0, "avg_accuracy": 0.0, "avg_time_taken": 0.0
            }

        # 3. ดึงค่ามาคำนวณและอัปเดตตามปกติ
        stats = save.data["player"]["historical_stats"][difficulty_mode]
        old_plays = stats["plays"]
        stats["plays"] += 1
        if success[0]:
            stats["wins"] += 1

        stats["avg_accuracy"] = ((stats["avg_accuracy"] * old_plays) + match_accuracy) / stats["plays"]
        stats["avg_time_taken"] = ((stats["avg_time_taken"] * old_plays) + catch_duration) / stats["plays"]
    # --------------------------------------------------------

    if success[0]:
        play_caught_sfx()
        if not fish_encounter["name"] in save.data["player"]["catched_fish"]:
            save.data["player"]["catched_fish"].append(fish_encounter["name"])
        save.data["player"]["total_catched"] += 1
        save.data["player"]["catched_streak"] += 1
        if is_perfect_catch:
            save.data["player"]["perfect_catches"] += 1
        save.save()
    else:
        play_failed_sfx()
        save.data["player"]["catched_streak"] = 0
        save.save()

    stop_reeling_sfx()

    if rod_using["name"] == "Meme Rod":
        stop_meme_sfx()

    if rod_using["name"] == "Meme Rod" and success[0] is True and 3 in choices:
        trigger_jumpscare(meme_fish=False)
        run_end_screen_meme(screen, clock, duration=4, meme_fish=False)

    if fish_encounter["name"] == "Meme Fish" and success[0] is False:
        trigger_jumpscare(meme_fish=True)
        run_end_screen_meme(screen, clock, duration=4, meme_fish=True)

    # Create buttons based on mode
    if is_experiment:
        continue_button = Button(
            rect=(
                S.WIDTH // 2 - button_width // 2,
                y_pos,
                button_width,
                button_height
            ),
            text="CONTINUE",
            font=btn_font,
            image=button_img
        )
    else:
        retry_button = Button(
            rect=(
                start_x,
                y_pos,
                button_width,
                button_height
            ),
            text="RETRY",
            font=btn_font,
            image=button_img
        )

        lobby_button = Button(
            rect=(
                start_x + button_width + button_gap,
                y_pos,
                button_width,
                button_height
            ),
            text="LOBBY",
            font=btn_font,
            image=button_img
        )
    result_running = True
    while result_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # แก้บรรทัดนี้: เพิ่ม match_accuracy และ baseline_skill ต่อท้ายเข้าไป
                return "QUIT" if not is_experiment else (success, catch_duration, match_accuracy, baseline_skill)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_experiment:
                    if continue_button.clicked(event):
                        return (success, catch_duration, match_accuracy, baseline_skill)
                else:
                    if retry_button.clicked(event):
                        return "RETRY"
                    if lobby_button.clicked(event):
                        return "LOBBY"

        screen.blit(bg_img2, (0, 0))

        if success[0]:
            # Display fish info
            msg = f"You caught a {fish_encounter['rarity']} {fish_encounter['name']}!"
            text_surf = font.render(msg, True, (200, 200, 200))
            text_rect = text_surf.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2 - 150 * S.scale))
            screen.blit(text_surf, text_rect)

            # Load and display fish image
            fish_image_path = os.path.join(ROOT_DIR, "assets", "images", "fishes", fish_encounter['img'])
            try:
                fish_img = pygame.image.load(fish_image_path).convert_alpha()
                img_width, img_height = fish_img.get_size()
                scaled_img = pygame.transform.scale(fish_img, (int(img_width * 0.75), int(img_height * 0.75)))
                img_rect = scaled_img.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2))
                screen.blit(scaled_img, img_rect)
            except pygame.error:
                # Fallback if image not found
                fallback_text = font.render("(Image not found)", True, (200, 200, 200))
                fallback_rect = fallback_text.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2))
                screen.blit(fallback_text, fallback_rect)

        else:
            msg = "The fish got away..."
            text_surf = font.render(msg, True, (200, 200, 200))
            text_rect = text_surf.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2))
            screen.blit(text_surf, text_rect)

        # Draw buttons
        if is_experiment:
            continue_button.draw(screen)
        else:
            retry_button.draw(screen)
            lobby_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
