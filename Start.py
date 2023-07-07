import pygame
from sys import exit
pygame.init()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800,400))
sky_surface = pygame.image.load("graphics/Sky.png")
ground_surface = pygame.image.load('graphics/Ground.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))



    pygame.display.update()
    clock.tick(60)