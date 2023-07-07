import pygame
from random import randint
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

def obstacle_movement(obstacle_list):



    if obstacle_list:
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 5

            if(obstacle_rectangle.y == 264):
                screen.blit(snail_surface,obstacle_rectangle)
            else:
                print(obstacle_rectangle.y)
                screen.blit(fly_surface,obstacle_rectangle)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list;
    else:
        return []
    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle): return False
    return True


screen = pygame.display.set_mode((800,400))
sky_surface = pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

# score_surface = test_font.render("My Game",False,(64,64,64))
# score_rectangle = score_surface.get_rect(center = (400,50))

#Obstacles
fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()

obstacle_rectangle_list = []

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

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1400)

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
                
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rectangle_list.append(snail_surface.get_rect(midbottom = (randint(900,1100),300)))
            else:
                obstacle_rectangle_list.append(fly_surface.get_rect(midbottom = (randint(900,1100),210)))
                     
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        # pygame.draw.rect(screen,'#c0e8ec',score_rectangle)
        # screen.blit(score_surface,score_rectangle)

        #Snail
        # screen.blit(snail_surface,snail_rectangle)
        # snail_rectangle.x -= 5;
        # if(snail_rectangle.right < -100):snail_rectangle.x= 800

        #Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300: player_rectangle.bottom = 300
        screen.blit(player_surface,player_rectangle)

        #Obstacle Movemenet
        obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        #Collision

        game_active = collisions(player_rectangle,obstacle_rectangle_list)
        # if snail_rectangle.colliderect(player_rectangle):
        #     score = int(pygame.time.get_ticks() / 1000) - gameTime
        #     game_active = False

        displayScore()
    else:
        obstacle_rectangle_list.clear()
        screen.fill((94,129,162))
        player_rectangle.midbottom = (50,300)
        player_gravity = 0;
        screen.blit(instruct_surface,instruct_rectangle)
        screen.blit(player_stand,player_stand_rectangle)
        if(score != 0):
            updateScore();

    
    pygame.display.update()
    clock.tick(60)