import pygame
import os

from gameData.config import BG_COLOR
from gameData.get_info import get_fish_data, get_locked_fish_info  
from utils.gadgets import Button, FishCard
from utils.load_img import load_ui_image    

# ── PATH ───────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)


FONT_TITLE = os.path.join(ROOT_DIR, "assets", "fonts", "Underlines-PVjX2.ttf")
FONT_BODY  = os.path.join(ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf")

FONT_PATH = os.path.join(
    ROOT_DIR, "assets", "fonts", "RasterForgeRegular-JpBgm.ttf"
)

PAGE_SIZE = 4  # 2x2

def run_bestiary(screen, S, unlocked_fish, FPS=60):
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Bestiary")
    clock = pygame.time.Clock()

    button_img = load_ui_image("button.png")
    bg_img = load_ui_image("bg.png")
    bg_img = pygame.transform.scale(bg_img, (S.WIDTH, S.HEIGHT))

    # fonts
    title_font = pygame.font.Font(FONT_PATH, int(48*S.scale))
    card_font = pygame.font.Font(FONT_PATH, int(16*S.scale)) 
    desc_font = pygame.font.Font(FONT_PATH, int(12*S.scale)) 
    btn_font = pygame.font.Font(FONT_PATH, int(26*S.scale)) 

    # data
    FISH_DATA = get_fish_data()
    LOCKED_INFO = get_locked_fish_info()
    fish_list = list(FISH_DATA.values())

    # layout
    CARD_W = int(S.WIDTH * 0.42)
    CARD_H = int(S.HEIGHT * 0.25)

    GAP_X = 26 * S.scale
    GAP_Y = 26 * S.scale

    START_X = (S.WIDTH - (CARD_W * 2 + GAP_X)) // 2
    START_Y = int(S.HEIGHT * 0.22)

    PAGE_SIZE = 4
    page = 0

    preview_image = None

    # buttons
    back_btn = Button(
        rect=(S.WIDTH * 0.18 - 80, S.HEIGHT * 0.80, 160, 80),
        text="BACK",
        font=btn_font,
        image=button_img
    )

    next_btn = Button(
        rect=(S.WIDTH * 0.82 - 80, S.HEIGHT * 0.80, 160, 80),
        text="NEXT",
        font=btn_font,
        image=button_img
    )

    center_btn = Button(
        rect=(S.WIDTH // 2 - 90, S.HEIGHT * 0.80, 180, 80),
        text="LOBBY",
        font=btn_font,
        image=button_img
    )

    # ── CREATE FISH CARDS (ONCE) ─────
    cards = []

    for rarity_group in fish_list:
        for fish in rarity_group:
            name = fish["name"]

            if name in unlocked_fish:
                data = fish
                img_path = os.path.join(
                    ROOT_DIR, "assets", "images", "fishes",
                    fish.get("img", "default.png")
                )
            else:
                locked_info = LOCKED_INFO.get(name, {})
                data = {
                    "name": "LOCKED FISH",
                    "desc": locked_info.get(
                        "desc", "Catch this fish to unlock information."
                    ),
                    "rarity": "Locked"
                }
                img_path = os.path.join(
                    ROOT_DIR, "assets", "images", "fishes",
                    locked_info.get("img", "locked_fish.png")
                )

            image = pygame.image.load(img_path).convert_alpha()

            cards.append(
                FishCard(
                    rect=(0, 0, CARD_W, CARD_H),  # set ตอน draw
                    fish_data=data,
                    font=card_font,
                    small_font=desc_font,
                    image=image,
                    rarity=data.get("rarity", "Common")
                )
            )

    # ── LOOP ────────────────────────
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "QUIT"

            # close preview
            if preview_image:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    preview_image = None
                continue

            start = page * PAGE_SIZE
            visible = cards[start:start + PAGE_SIZE]

            # click image → preview
            for c in visible:
                if c.image_clicked(event):
                    preview_image = c.image
                    break

            if back_btn.clicked(event) and page > 0:
                page -= 1

            if next_btn.clicked(event) and (page + 1) * PAGE_SIZE < len(cards):
                page += 1

            if center_btn.clicked(event):
                return "LOBBY"

        # ── DRAW ─────────────────────
        screen.blit(bg_img, (0, 0))

        title = title_font.render("Bestiary", True, (51,25,0))
        screen.blit(
            title,
            title.get_rect(center=(S.WIDTH // 2, S.HEIGHT * 0.12))
        )

        start = page * PAGE_SIZE
        visible = cards[start:start + PAGE_SIZE]

        for i, card in enumerate(visible):
            col = i % 2
            row = i // 2

            x = START_X + col * (CARD_W + GAP_X)
            y = START_Y + row * (CARD_H + GAP_Y)

            card.rect.topleft = (x, y)
            card.draw(screen)

        back_btn.draw(screen)
        center_btn.draw(screen)
        next_btn.draw(screen)

        # preview overlay
        if preview_image:
            overlay = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            big = pygame.transform.smoothscale(
                preview_image,
                (int(S.WIDTH * 0.97), int(S.HEIGHT * 0.7))
            )
            rect = big.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2))
            screen.blit(big, rect)

            screen.blit(card_font.render(
            f"[Click anywhere to close preview]",
            True, (200, 200, 200)), ((S.WIDTH // 2 ) - (card_font.size(f"[Click anywhere to close preview]")[0] // 2), S.HEIGHT * 0.87))

        pygame.display.flip()
        clock.tick(FPS)
