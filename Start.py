import pygame
from sys import exit
pygame.init()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/ysp.ttf',50)


screen = pygame.display.set_mode((800,400))
sky_surface = pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()
text_surface = test_font.render("My Game",False,'Black')

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom = (800,300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (50,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface,(300,50))

    
    screen.blit(snail_surface,snail_rectangle)
    snail_rectangle.x -= 5;
    if(snail_rectangle.right < -100):snail_rectangle.x= 800


    screen.blit(player_surface,player_rectangle)

    if player_rectangle.colliderect(snail_rectangle):
        print("collision")
    
    pygame.display.update()
    clock.tick(60)