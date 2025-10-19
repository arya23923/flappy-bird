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

bird = pygame.image.load("./images/bird.png")
bird = pygame.transform.scale(bird, (50, 50))
bird_speed = 8
bird_x = screen.get_width() / 2 - 400
bird_y = screen.get_height() / 2

pipe = pygame.image.load('./images/pipe.png')
pipe = pygame.transform.scale(pipe, (350, 350))
pipe_x = screen.get_width()
pipe_y = screen.get_height() 

pipe_ulta = pygame.image.load('./images/pipe-ulta.png')
pipe_ulta = pygame.transform.scale(pipe, (350, 350))
# pipe_x = screen.get_width()
# pipe_y = screen.get_height() 


while running:

    clock.tick(50)

    if bird_y > screen.get_height() : running = False

    i = 0
    while(i<tiles):
        screen.blit(bg, (bg.get_width()*i + scroll, 0))
        screen.blit(pipe, (pipe.get_width()*i + scroll, 0))
        screen.blit(pipe_ulta, (pipe_ulta.get_width()*i + scroll, screen.get_height() + 40))
        i+=1
    
    scroll -= 6

    if abs(scroll) > bg.get_width():
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]: 
        bird_y -= bird_speed * 2
    bird_y += bird_speed

    screen.blit(bird, (bird_x, bird_y))
    

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    
    pygame.display.update()
    


pygame.quit()


 