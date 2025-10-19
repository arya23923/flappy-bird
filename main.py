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
bird_x = 200
bird_y = screen.get_height() // 2

pipe = pygame.image.load('./images/pipe.png')
pipe = pygame.transform.scale(pipe, (180, 400))
pipe_ulta = pygame.image.load('./images/pipe-ulta.png')
pipe_ulta = pygame.transform.scale(pipe_ulta, (180, 400))

PIPE_WIDTH = 180
PIPE_HEIGHT = 400
GAP_HEIGHT = 140      
PIPE_SPACING = 350
SCROLL_SPEED = 5

def create_pipes():
    pipes = []
    min_gap_y = 150                   
    max_gap_y = screen.get_height() - 150  
    for i in range(6):
        x = 700 + i * PIPE_SPACING
        gap_y = random.randint(min_gap_y, max_gap_y)
        pipes.append([x, gap_y])
    return pipes


pipes = create_pipes()

while running:
    clock.tick(40)
    screen.fill((0, 0, 0))

    i = 0
    while i < tiles:
        screen.blit(bg, (bg.get_width() * i + scroll, 0))
        i += 1
    scroll -= 2
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
        top_pipe_bottom = gap_y - (GAP_HEIGHT // 2)
        bottom_pipe_top = gap_y + (GAP_HEIGHT // 2)

        screen.blit(pipe_ulta, (pipe_x, top_pipe_bottom - PIPE_HEIGHT))
        screen.blit(pipe, (pipe_x, bottom_pipe_top))

        pipe_data[0] -= SCROLL_SPEED

        if pipe_data[0] < -PIPE_WIDTH:
            pipe_data[0] = max([p[0] for p in pipes]) + PIPE_SPACING
            pipe_data[1] = random.randint(150, screen.get_height() - 150)


    screen.blit(bird, (bird_x, bird_y))

    if bird_y > screen.get_height():
        running = False

    pygame.display.flip()

pygame.quit()
