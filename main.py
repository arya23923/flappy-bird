import pygame
import random
import math

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Background
bg = pygame.image.load('./images/sky.jpg').convert()
scroll = 0
tiles = math.ceil(1280 / bg.get_width()) + 1

# Bird
bird = pygame.image.load("./images/bird.png")
bird = pygame.transform.scale(bird, (50, 50))
bird_speed = 8
bird_x = 200
bird_y = screen.get_height() // 2

# Pipes
pipe = pygame.image.load('./images/pipe.png')
pipe = pygame.transform.scale(pipe, (180, 400))
pipe_ulta = pygame.image.load('./images/pipe-ulta.png')
pipe_ulta = pygame.transform.scale(pipe_ulta, (180, 400))

PIPE_WIDTH = 180
PIPE_HEIGHT = 400
GAP_HEIGHT = 180
PIPE_SPACING = 350
SCROLL_SPEED = 5

# Create multiple pipe pairs
def create_pipes():
    pipes = []
    min_gap_y = PIPE_HEIGHT // 2 + GAP_HEIGHT // 2
    max_gap_y = screen.get_height() - (PIPE_HEIGHT // 2 + GAP_HEIGHT // 2)
    for i in range(6):
        x = 700 + i * PIPE_SPACING
        gap_y = random.randint(min_gap_y, max_gap_y)
        pipes.append([x, gap_y])
    return pipes

pipes = create_pipes()

# Game loop
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    # Background scroll
    i = 0
    while i < tiles:
        screen.blit(bg, (bg.get_width() * i + scroll, 0))
        i += 1
    scroll -= 2
    if abs(scroll) > bg.get_width():
        scroll = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Bird movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird_y -= bird_speed * 2
    bird_y += bird_speed

    # Draw pipes and scroll them
    for pipe_data in pipes:
        pipe_x, gap_y = pipe_data
        top_pipe_bottom = gap_y - (GAP_HEIGHT // 2)
        bottom_pipe_top = gap_y + (GAP_HEIGHT // 2)

        # Draw top pipe (flipped)
        screen.blit(pipe_ulta, (pipe_x, top_pipe_bottom - PIPE_HEIGHT))
        # Draw bottom pipe
        screen.blit(pipe, (pipe_x, bottom_pipe_top))

        # Move pipe
        pipe_data[0] -= SCROLL_SPEED

        # Recycle pipe when off-screen
        if pipe_data[0] < -PIPE_WIDTH:
            pipe_data[0] = screen.get_width() + PIPE_SPACING
            min_gap_y = PIPE_HEIGHT // 2 + GAP_HEIGHT // 2
            max_gap_y = screen.get_height() - (PIPE_HEIGHT // 2 + GAP_HEIGHT // 2)
            pipe_data[1] = random.randint(min_gap_y, max_gap_y)

    # Draw bird
    screen.blit(bird, (bird_x, bird_y))

    # End game if bird falls off screen
    if bird_y > screen.get_height():
        running = False

    pygame.display.flip()

pygame.quit()
