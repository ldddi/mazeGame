import pygame
import config
import game_manager
from utils.draw_text import draw_text
# pygame setup
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

game_manager = game_manager.GameManager(screen)

running = True
success_time = -1
success_finish = False
pygame.mixer.music.load("static/sound/bgm.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
icon = pygame.image.load('static/images/maze.png').convert()
pygame.display.set_icon(icon)
pygame.display.set_caption("汽车迷宫")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif success_finish and event.type == pygame.KEYDOWN:
            running = False

    screen.fill("black")

    if success_finish:
        screen.fill("black")
        draw_text(screen, "Win!", 200, config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
    else:
        if success_time >= 0:
            if pygame.time.get_ticks() - success_time > 2000:
                has_next = game_manager.next_level()
                if not has_next:
                    success_finish = True
                    continue
                success_time = -1

        if game_manager.update():
            success_time = pygame.time.get_ticks()

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
