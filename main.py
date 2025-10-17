import pygame
import random

# Initialize setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Load assets
bg = pygame.image.load('./images/sky.jpg').convert()
bird = pygame.image.load("./images/bird.png")
bird = pygame.transform.scale(bird, (50, 50))
bird_speed = 8
bird_x = 200
bird_y = screen.get_height() // 2

pipe_img = pygame.image.load('./images/pipe.png')
pipe_img = pygame.transform.scale(pipe_img, (180, 600))  # thicker width
pipe_ulta_img = pygame.image.load('./images/pipe-ulta.png')
pipe_ulta_img = pygame.transform.scale(pipe_ulta_img, (180, 600))  # thicker width

# Pipe properties
PIPE_WIDTH = 180
PIPE_HEIGHT = 600
GAP_HEIGHT = 100   # more space between top and bottom pipes
PIPE_SPACING = 350
SCROLL_SPEED = 4

# Create pipes
pipes = []
for i in range(4):
    x = 700 + i * PIPE_SPACING
    offset = random.randint(200, 400)  # fixed offset range prevents floating pipes
    pipes.append([x, offset])

def reset_game():
    """Resets bird and pipe positions."""
    global bird_x, bird_y, pipes
    bird_x = 200
    bird_y = screen.get_height() // 2
    pipes = []
    for i in range(5):
        x = 700 + i * PIPE_SPACING
        offset = random.randint(200, 400)
        pipes.append([x, offset])

# Game loop
running = True
while running:
    clock.tick(40)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird_y -= bird_speed * 2
    bird_y += bird_speed

    # Scroll pipes
    for pipe in pipes:
        pipe_x, pipe_offset = pipe
        # Top pipe (flipped)
        screen.blit(pipe_ulta_img, (pipe_x, pipe_offset - PIPE_HEIGHT))
        # Bottom pipe (normal)
        screen.blit(pipe_img, (pipe_x, pipe_offset + GAP_HEIGHT))
        pipe[0] -= SCROLL_SPEED

        # Move off-screen pipes to right
        if pipe[0] < -PIPE_WIDTH:
            pipe[0] = screen.get_width()
            pipe[1] = random.randint(200, 400)

    # Draw bird
    screen.blit(bird, (bird_x, bird_y))

    # Gameover condition
    if bird_y > screen.get_height():
        running = False

    pygame.display.flip()

pygame.quit()
