import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
bg = pygame.image.load('./images/sky.jpg').convert()

scroll = 0
tiles = math.ceil(1280 / bg.get_width()) + 1

bird = pygame.image.load("./images/bird.png")
bird = pygame.transform.scale(bird, (50, 50))
bird_speed = 8
bird_x = screen.get_width() / 2 - 400
bird_y = screen.get_height() / 2

pipe = pygame.image.load('./images/pipe.png')
pipe = pygame.transform.scale(pipe, (180, 600))
pipe_ulta = pygame.image.load('./images/pipe-ulta.png')
pipe_ulta = pygame.transform.scale(pipe_ulta, (180, 600))

PIPE_WIDTH = 180
PIPE_HEIGHT = 600
GAP_HEIGHT = 100
PIPE_SPACING = 350
SCROLL_SPEED = 6

def create_pipes():
    pipes = []
    for i in range(6):
        x = 700 + i * PIPE_SPACING
        gap_y = random.randint(200, screen.get_height() - 200 - GAP_HEIGHT)
        pipes.append([x, gap_y])
    return pipes

pipes = create_pipes()

while running:
    clock.tick(40)
    if bird_y > screen.get_height():
        running = False

    for i in range(tiles):
        screen.blit(bg, (bg.get_width() * i + scroll, 0))
    scroll -= SCROLL_SPEED
    if abs(scroll) > bg.get_width():
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird_y -= bird_speed * 2
    bird_y += bird_speed

    for pipe_data in pipes:
        pipe_x, gap_y = pipe_data

        top_y = gap_y - PIPE_HEIGHT
        screen.blit(pipe_ulta, (pipe_x, top_y))

        bottom_y = gap_y + GAP_HEIGHT
        screen.blit(pipe, (pipe_x, bottom_y))

        pipe_data[0] -= SCROLL_SPEED

        if pipe_data[0] < -PIPE_WIDTH:
            pipe_data[0] = max([p[0] for p in pipes]) + PIPE_SPACING
            pipe_data[1] = random.randint(200, screen.get_height() - 200 - GAP_HEIGHT)

    screen.blit(bird, (bird_x, bird_y))

    pygame.display.flip()

pygame.quit()
