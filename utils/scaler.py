import pygame
import gameData.config as C


class ScaledConfig:
    pass


def build_scaled_config(width, height, orientation="horizontal"):

    s = ScaledConfig()

    # ─────────────────────────
    # SCREEN
    # ─────────────────────────
    s.WIDTH = width
    s.HEIGHT = height
    s.orientation = orientation

    # scale factor (reference only)
    s.scale = min(
        width / C.BASE_WIDTH,
        height / C.BASE_HEIGHT
    )

    # ─────────────────────────
    # TRACK
    # ─────────────────────────

    if orientation == "horizontal":

        s.TRACK_WIDTH = int(width * 0.85)
        s.TRACK_HEIGHT = int(height * 0.07)

        s.TRACK_X = width // 2 - s.TRACK_WIDTH // 2
        s.TRACK_Y = int(height * 0.75)

    else:  # VERTICAL

        s.TRACK_HEIGHT = int(height * 0.75)
        s.TRACK_WIDTH = int(width * 0.1)

        s.TRACK_X = width // 2 - s.TRACK_WIDTH // 2
        s.TRACK_Y = height // 2 - s.TRACK_HEIGHT // 2

    # ─────────────────────────
    # BAR (mirror logic)
    # ─────────────────────────

    if orientation == "horizontal":

        s.BAR_WIDTH = int(s.TRACK_WIDTH * 0.25)
        s.BAR_HEIGHT = s.TRACK_HEIGHT

        s.BAR_MIN_X = s.TRACK_X
        s.BAR_MAX_X = s.TRACK_X + s.TRACK_WIDTH - s.BAR_WIDTH

    else:  # VERTICAL

        s.BAR_WIDTH = s.TRACK_WIDTH
        s.BAR_HEIGHT = int(s.TRACK_HEIGHT * 0.25)

        s.BAR_MIN_Y = s.TRACK_Y
        s.BAR_MAX_Y = s.TRACK_Y + s.TRACK_HEIGHT - s.BAR_HEIGHT

    # ─────────────────────────
    # FISH
    # ─────────────────────────

    s.FISH_SIZE = int(min(width, height) * 0.015)

    # ─────────────────────────
    # PROGRESS BAR
    # ─────────────────────────

    if orientation == "horizontal":

        s.PROGRESS_BAR_WIDTH = int(s.TRACK_WIDTH * 0.6)
        s.PROGRESS_BAR_HEIGHT = int(height * 0.02)

        s.PROGRESS_BAR_X = width // 2 - s.PROGRESS_BAR_WIDTH // 2
        s.PROGRESS_BAR_Y = (
            s.TRACK_Y + s.TRACK_HEIGHT + int(height * 0.03)
        )

    else:  # VERTICAL

        s.PROGRESS_BAR_WIDTH = int(width * 0.04)
        s.PROGRESS_BAR_HEIGHT = int(s.TRACK_HEIGHT * 0.6)

        s.PROGRESS_BAR_X = (
            s.TRACK_X + s.TRACK_WIDTH + int(width * 0.03)
        )

        s.PROGRESS_BAR_Y = (
            height // 2 - s.PROGRESS_BAR_HEIGHT // 2
        )

    # ─────────────────────────
    # COPY LOGIC FROM CONFIG
    # ─────────────────────────

    s.BAR_MAX_SPEED = C.BAR_MAX_SPEED
    s.BAR_FRICTION = C.BAR_FRICTION
    s.BAR_FORCE_INC = C.BAR_FORCE_INC
    s.BAR_FORCE_DEC = C.BAR_FORCE_DEC
    s.BAR_FORCE_MAX = C.BAR_FORCE_MAX
    s.BAR_DRIFT_LEFT = C.BAR_DRIFT_LEFT
    s.BAR_DRIFT_DOWN = C.BAR_DRIFT_DOWN

    s.PROGRESS_INIT = C.PROGRESS_INIT
    s.PROGRESS_FILL_ANIM_SPEED = C.PROGRESS_FILL_ANIM_SPEED
    s.PROGRESS_UP_RATE = C.PROGRESS_UP_RATE
    s.PROGRESS_DOWN_RATE = C.PROGRESS_DOWN_RATE

    s.FISH_MOVE_MIN_DIST = C.FISH_MOVE_MIN_DIST
    s.FISH_MOVE_MAX_DIST = C.FISH_MOVE_MAX_DIST
    s.FISH_MIN_SPEED = C.FISH_MIN_SPEED
    s.FISH_MAX_SPEED = C.FISH_MAX_SPEED

    s.ENCOUNTER_FREEZE_TIME = C.ENCOUNTER_FREEZE_TIME

    return s
