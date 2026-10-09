from matplotlib import image
import pygame

from utils.load_audio import play_button_sfx

RARITY_COLORS = {
    "Common":     (180, 180, 180),
    "Uncommon":   (120, 220, 120),
    "Rare":       (100, 180, 255),
    "Legendary":  (255, 200, 80),
    "Mythical":   (220, 120, 255),
    "Meme":       (255, 100, 120),
    "Locked":     (90, 90, 90)
}

# ── BUTTON CLASS ──────────────────
class Button:
    def __init__(self, rect, text, font, image, text_color=(51,25,0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.text_color = text_color

        base_img = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        self.image = base_img
        self.hover_image = brighten(base_img)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hover_image, self.rect)
            corner_color = (255, 200, 60)
            thickness = 5
            length = 18
            r = -1  # offset radius from the corner

            x, y, w, h = self.rect

            # ── Top Left ──
            pygame.draw.line(screen, corner_color, (x-r, y-r), (x-r+length, y-r), thickness)
            pygame.draw.line(screen, corner_color, (x-r, y-r), (x-r, y-r+length), thickness)

            # ── Top Right ──
            pygame.draw.line(screen, corner_color, (x+w+r, y-r), (x+w+r-length, y-r), thickness)
            pygame.draw.line(screen, corner_color, (x+w+r, y-r), (x+w+r, y-r+length), thickness)

            # ── Bottom Left ──
            pygame.draw.line(screen, corner_color, (x-r, y+h+r), (x-r+length, y+h+r), thickness)
            pygame.draw.line(screen, corner_color, (x-r, y+h+r), (x-r, y+h+r-length), thickness)

            # ── Bottom Right ──
            pygame.draw.line(screen, corner_color, (x+w+r, y+h+r), (x+w+r-length, y+h+r), thickness)
            pygame.draw.line(screen, corner_color, (x+w+r, y+h+r), (x+w+r, y+h+r-length), thickness)
        else:
            screen.blit(self.image, self.rect)

        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                play_button_sfx()
                return True
        return False


# ── SWITCH BUTTON ─────────────────────────────
class Switch:
    def __init__(self, rect, left_text, right_text, font, initial=True):
        self.rect = pygame.Rect(rect)
        self.left_text = left_text
        self.right_text = right_text
        self.font = font
        self.value = initial  # True = left, False = right

        self.bg_color = (224, 150, 40)
        self.active_color = (255, 210, 85)
        self.text_color = (51,25,0)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.value = not self.value
                return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=8)

        half_w = self.rect.width // 2

        active_rect = pygame.Rect(
            self.rect.x if self.value else self.rect.x + half_w,
            self.rect.y,
            half_w,
            self.rect.height
        )

        pygame.draw.rect(screen, self.active_color, active_rect, border_radius=8)
        pygame.draw.line(
            screen,
            (51,25,0),
            (self.rect.centerx, self.rect.y + 3),
            (self.rect.centerx, self.rect.bottom - 3),
            3
        )

        left_surf = self.font.render(self.left_text, True, self.text_color)
        right_surf = self.font.render(self.right_text, True, self.text_color)

        screen.blit(
            left_surf,
            left_surf.get_rect(center=(self.rect.x + half_w // 2,
                                       self.rect.centery))
        )

        screen.blit(
            right_surf,
            right_surf.get_rect(center=(self.rect.x + half_w + half_w // 2,
                                       self.rect.centery))
        )

        pygame.draw.rect(screen, (80, 40, 0), self.rect, 3, border_radius=8)

class Slider:
    def __init__(self, rect, min_val, max_val, start_val):
        self.rect = pygame.Rect(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val

        self.dragging = False
        self.handle_radius = 10

    def draw(self, screen):

        # --- Track ---
        track_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )

        pygame.draw.rect(screen, (224, 150, 40), track_rect, border_radius=4)
        pygame.draw.rect(screen, (51,25,0), track_rect, 2, border_radius=4)

        # --- Fill  ---
        fill_width = int((self.value - self.min_val) /
                        (self.max_val - self.min_val) * self.rect.width)

        fill_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            fill_width,
            self.rect.height
        )

        pygame.draw.rect(screen, (51,25,0), fill_rect, border_radius=4)

        # --- Handle  ---
        handle_width = 18
        handle_rect = pygame.Rect(
            self.rect.x + fill_width - handle_width // 2,
            self.rect.y - 4,
            handle_width,
            self.rect.height + 8
        )

        pygame.draw.rect(screen, (255, 210, 85), handle_rect, border_radius=4)
        pygame.draw.rect(screen, (51,25,0), handle_rect, 2, border_radius=4)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            x = max(self.rect.x, min(event.pos[0], self.rect.right))
            ratio = (x - self.rect.x) / self.rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)



# ── FISH CARD CLASS ────────────────
class FishCard:
    def __init__(self, rect, fish_data, font, small_font,
                 image=None, rarity="Common"):
        self.rect = pygame.Rect(rect)
        self.fish = fish_data
        self.font = font
        self.small_font = small_font
        self.image = image
        self.rarity = rarity

        # ── RARITY COLOR ─────────────────
        self.rarity_color = RARITY_COLORS.get(rarity, (180, 180, 180))

        # ── IMAGE BOX CONFIG  ─────────
        self.IMG_BOX_W = 120     
        self.IMG_BOX_H = 90
        self.IMG_PAD_TOP = 40

        self.img_rect = None     #  click 

    def draw(self, screen):
        # ── CARD BACKGROUND (40, 60, 90)──────────────
        pygame.draw.rect(
            screen,
            (255, 255, 204),
            self.rect,
            border_radius=18
        )

        # Outer Border
        pygame.draw.rect(screen, (90, 50, 0), self.rect, 4, border_radius=18)

        # Inner Border 
        # inner_rect = self.rect.inflate(-6, -6)
        # pygame.draw.rect(screen, self.rarity_color, inner_rect, 3, border_radius=14)

        # ── TITLE  ────────────────────────
        title = self.font.render(
            self.fish["name"].upper(),
            True,
            self.rarity_color
        )
        title_rect = title.get_rect(
            centerx=self.rect.centerx,
            y=self.rect.y + 14
        )
        screen.blit(title, title_rect)

        # ── IMAGE AREA  ─
        img_x = self.rect.centerx - self.IMG_BOX_W // 2
        img_y = self.rect.y + self.IMG_PAD_TOP

        if self.image:
            img = scale_to_fit(
                self.image,
                self.IMG_BOX_W,
                self.IMG_BOX_H
            )
            self.img_rect = img.get_rect(
                center=(
                    self.rect.centerx,
                    img_y + self.IMG_BOX_H // 2
                )
            )

            # border
            pygame.draw.rect(
                screen,
                self.rarity_color,
                self.img_rect.inflate(6, 6),
                3,
                border_radius=8
            )

            screen.blit(img, self.img_rect)
        else:
            self.img_rect = pygame.Rect(
                img_x, img_y,
                self.IMG_BOX_W,
                self.IMG_BOX_H
            )
            pygame.draw.rect(
                screen,
                (30, 30, 30),
                self.img_rect,
                border_radius=8
            )

        # ── DESCRIPTION ─
        desc_y = self.img_rect.bottom + 12
        self.draw_multiline_text_center(
            screen,
            self.fish.get("desc", "").upper(),
            self.rect.centerx,
            desc_y,
            self.small_font,
            self.rect.width - 32
        )

        mouse_pos = pygame.mouse.get_pos()
        is_hover_img = self.img_rect and self.img_rect.collidepoint(mouse_pos)
        if is_hover_img:
            corner_color = (51, 25, 0)
            thickness = 3
            length = 14

            x, y, w, h = self.img_rect

            pygame.draw.line(screen, corner_color, (x, y), (x+length, y), thickness)
            pygame.draw.line(screen, corner_color, (x, y), (x, y+length), thickness)

            pygame.draw.line(screen, corner_color, (x+w, y), (x+w-length, y), thickness)
            pygame.draw.line(screen, corner_color, (x+w, y), (x+w, y+length), thickness)

            pygame.draw.line(screen, corner_color, (x, y+h), (x+length, y+h), thickness)
            pygame.draw.line(screen, corner_color, (x, y+h), (x, y+h-length), thickness)

            pygame.draw.line(screen, corner_color, (x+w, y+h), (x+w-length, y+h), thickness)
            pygame.draw.line(screen, corner_color, (x+w, y+h), (x+w, y+h-length), thickness)

    # ── CLICK CHECK ─────────────────
    def image_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.img_rect
            and self.img_rect.collidepoint(event.pos)
        )

    # ── TEXT WRAP CENTER ─────────────────
    def draw_multiline_text_center(
        self, surface, text, center_x, start_y, font, max_width
    ):
        words = text.split(" ")
        lines, line = [], ""

        for w in words:
            test = line + w + " "
            if font.size(test)[0] <= max_width:
                line = test
            else:
                lines.append(line)
                line = w + " "

        if line:
            lines.append(line)

        y = start_y
        for ln in lines:
            surf = font.render(ln.strip(), True, (51,25,0))
            rect = surf.get_rect(centerx=center_x, y=y)
            surface.blit(surf, rect)
            y += font.get_height() + 4


# ── ROD CARD CLASS ────────────────
class RodCard:
    def __init__(self, rect, rod_data, font, small_font,
                 selected=False, image=None):
        self.rect = pygame.Rect(rect)
        self.rod = rod_data
        self.font = font
        self.small_font = small_font
        self.selected = selected
        self.image = image

        # image box
        self.IMG_PAD = 24
        self.IMG_BOX_W = 110
        self.IMG_BOX_H = 140

        self.img_rect = None  # Check if clicked

    def draw(self, screen):
        bg = (255, 210, 85) if self.selected else (255, 255, 204)
        pygame.draw.rect(screen, bg, self.rect, border_radius=18)
        pygame.draw.rect(screen, (51,25,0), self.rect, 3, border_radius=18)

        if self.selected:
            corner_color = (255, 200, 60)
            thickness = 5
            length = 18
            r = 10  # offset radius from the corner

            x, y, w, h = self.rect

            # ── Top Left ──
            pygame.draw.line(screen, corner_color, (x-r, y-r), (x-r+length, y-r), thickness)
            pygame.draw.line(screen, corner_color, (x-r, y-r), (x-r, y-r+length), thickness)

            # ── Top Right ──
            pygame.draw.line(screen, corner_color, (x+w+r, y-r), (x+w+r-length, y-r), thickness)
            pygame.draw.line(screen, corner_color, (x+w+r, y-r), (x+w+r, y-r+length), thickness)

            # ── Bottom Left ──
            pygame.draw.line(screen, corner_color, (x-r, y+h+r), (x-r+length, y+h+r), thickness)
            pygame.draw.line(screen, corner_color, (x-r, y+h+r), (x-r, y+h+r-length), thickness)

            # ── Bottom Right ──
            pygame.draw.line(screen, corner_color, (x+w+r, y+h+r), (x+w+r-length, y+h+r), thickness)
            pygame.draw.line(screen, corner_color, (x+w+r, y+h+r), (x+w+r, y+h+r-length), thickness)

        # ── IMAGE ───────────────────
        img_x = self.rect.x + self.IMG_PAD
        img_y = self.rect.centery - self.IMG_BOX_H // 2

        if self.image:
            img = scale_to_fit(self.image, self.IMG_BOX_W, self.IMG_BOX_H)
            self.img_rect = img.get_rect(
                center=(img_x + self.IMG_BOX_W // 2,
                        img_y + self.IMG_BOX_H // 2)
            )
            screen.blit(img, self.img_rect)
        else:
            self.img_rect = pygame.Rect(img_x, img_y, self.IMG_BOX_W, self.IMG_BOX_H)
            pygame.draw.rect(screen, (30, 30, 30), self.img_rect, border_radius=8)
    
        # ── TEXT ────────────────────
        text_x = img_x + self.IMG_BOX_W + 24

        title = self.font.render(self.rod["name"].upper(), True, (51,25,0))
        screen.blit(title, (text_x, self.rect.y + 18))

        y = self.rect.y + 52
        stats = [
            ("LUCK", self.rod.get("LUCK")),
            ("CONTROL", self.rod.get("CONTROLLED")),
            ("RESILIENCE", self.rod.get("RESILIENCE")),
        ]

        for name, value in stats:

            if value is None:
                display_value = "N/A"
            else:
                if name == "CONTROL":
                    display_value = format_number(value)
                else:
                    display_value = format_percent(value)

            text = f"{name:<12} {display_value}"
            screen.blit(
                self.small_font.render(text, True, (51,25,0)),
                (text_x, y)
            )
            y += 22

        desc_lines = wrap_text(
            self.rod.get("desc", ""),
            self.small_font,
            self.rect.right - text_x - 24
        )

        dy = self.rect.bottom - 20 - len(desc_lines) * 18
        for ln in desc_lines:
            screen.blit(self.small_font.render(ln, True, (51,25,0)), (text_x, dy))
            dy += 18
        
        mouse_pos = pygame.mouse.get_pos()
        is_hover_img = self.img_rect and self.img_rect.collidepoint(mouse_pos)
        if is_hover_img:
            corner_color = (51, 25, 0)
            thickness = 3
            length = 14

            x, y, w, h = self.img_rect

            pygame.draw.line(screen, corner_color, (x, y), (x+length, y), thickness)
            pygame.draw.line(screen, corner_color, (x, y), (x, y+length), thickness)

            pygame.draw.line(screen, corner_color, (x+w, y), (x+w-length, y), thickness)
            pygame.draw.line(screen, corner_color, (x+w, y), (x+w, y+length), thickness)

            pygame.draw.line(screen, corner_color, (x, y+h), (x+length, y+h), thickness)
            pygame.draw.line(screen, corner_color, (x, y+h), (x, y+h-length), thickness)

            pygame.draw.line(screen, corner_color, (x+w, y+h), (x+w-length, y+h), thickness)
            pygame.draw.line(screen, corner_color, (x+w, y+h), (x+w, y+h-length), thickness)

    def image_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.img_rect
            and self.img_rect.collidepoint(event.pos)
        )
    


# ── HELPERS ─────────────────────────
def scale_to_fit(img, max_w, max_h):
    w, h = img.get_size()
    s = min(max_w / w, max_h / h)
    return pygame.transform.smoothscale(img, (int(w * s), int(h * s)))

def wrap_text(text, font, max_w):
    words = text.split(" ")
    lines, line = [], ""
    for w in words:
        test = line + w + " "
        if font.size(test)[0] <= max_w:
            line = test
        else:
            lines.append(line.strip())
            line = w + " "
    if line:
        lines.append(line.strip())
    return lines

def format_percent(value):
    if isinstance(value, (int, float)):
        return f"{value * 100:.0f}%"
    return "N/A"

def format_number(value):
    if isinstance(value, (int, float)):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return "N/A"

def scale_to_fit(image, max_w, max_h):
    w, h = image.get_size()
    scale = min(max_w / w, max_h / h)
    return pygame.transform.smoothscale(
        image,
        (int(w * scale), int(h * scale))
    )

def brighten(image, amount=40):
            img = image.copy()
            img.fill((amount, amount, amount, 0), special_flags=pygame.BLEND_RGBA_ADD)
            return img