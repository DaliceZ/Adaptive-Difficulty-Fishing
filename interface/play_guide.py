import pygame

from utils.load_img import load_tutorial


def run_play_guide(screen, S, duration=10, FPS=60):
    clock = pygame.time.Clock()

    img = pygame.transform.smoothscale(
            load_tutorial("guide.png"),
            (S.WIDTH, S.HEIGHT)
        )

    start_time = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        screen.blit(img, (0, 0))
        pygame.display.flip()

        current_time = pygame.time.get_ticks()
        if (current_time - start_time) > duration * 1000:
            running = False

    return  # back to caller