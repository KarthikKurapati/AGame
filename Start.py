import pygame
from sys import exit
pygame.init()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/ysp.ttf',50)
game_active = False
gameTime = 0;
score = 0;

def displayScore():
    current_time = int(pygame.time.get_ticks() / 1000)
    score_surface = test_font.render(f'{current_time - gameTime}',False,(64,64,64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)

def updateScore():
    score_title_surface = test_font.render("Score: " + str(score),False,(111,196,169))
    score_title_surface = pygame.transform.rotozoom(score_title_surface,0,0.5)
    score_title_rectangle = score_title_surface.get_rect(center = (400,300))
    screen.blit(score_title_surface,score_title_rectangle)

screen = pygame.display.set_mode((800,400))
sky_surface = pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

# score_surface = test_font.render("My Game",False,(64,64,64))
# score_rectangle = score_surface.get_rect(center = (400,50))

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom = (800,300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (50,300))
player_gravity = 0;

# Intro Screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(center = (400,150))

#Instructions
instruct_surface = test_font.render('Press SPACE to start!',False,(111,196,169))
instruct_surface = pygame.transform.rotozoom(instruct_surface,0,0.5)
instruct_rectangle = instruct_surface.get_rect(center = (400,350))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            exit()
        if game_active == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                gameTime = int(pygame.time.get_ticks() / 1000)
                snail_rectangle.x = 800
                     
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        # pygame.draw.rect(screen,'#c0e8ec',score_rectangle)
        # screen.blit(score_surface,score_rectangle)

        #Snail
        screen.blit(snail_surface,snail_rectangle)
        snail_rectangle.x -= 5;
        if(snail_rectangle.right < -100):snail_rectangle.x= 800

        #Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300: player_rectangle.bottom = 300
        screen.blit(player_surface,player_rectangle)

        #Collision
        if snail_rectangle.colliderect(player_rectangle):
            score = int(pygame.time.get_ticks() / 1000) - gameTime
            game_active = False

        displayScore()
    else:
        screen.fill((94,129,162))
        screen.blit(instruct_surface,instruct_rectangle)
        screen.blit(player_stand,player_stand_rectangle)
        if(score != 0):
            updateScore();

    
    pygame.display.update()
    clock.tick(60)