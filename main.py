import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

bg = pygame.image.load('./images/sky.jpg').convert()

scroll = 0 
tiles = math.ceil(1280  /bg.get_width()) + 1 

player_pos = pygame.Vector2(screen.get_width() / 2 - 500, screen.get_height() / 2)

while running:

    clock.tick(50)

    i = 0
    while(i<tiles):
        screen.blit(bg, (bg.get_width()*i + scroll, 0))
        i+=1
    
    scroll -= 6

    if abs(scroll) > bg.get_width():
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.circle(screen, "black", player_pos, 20)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    
    pygame.display.update()
    


pygame.quit()


 