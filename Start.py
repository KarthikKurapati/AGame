import random
import pygame
from sys import exit
pygame.init()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/ysp.ttf',50)
game_active = False
gameTime = 0;
global score;
score = 0;

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0;
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0;
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
    def apply_gravity(self):
        self.gravity += 1;
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1;
            if(self.player_index >= len(self.player_walk)): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            fly_index = 0;
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            snail_index = 0;
            y_pos = 300
        
        self.animation_index = 0;
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1000),y_pos))
    def animation_state(self):
        self.animation_index += 0.1;
        if(self.animation_index > len(self.frames)):self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

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
                screen.blit(fly_surface,obstacle_rectangle)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list;
    else:
        return []
    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle):
                return False
    return True

def playerAnimation():
    global player_surface,player_index
    if(player_rectangle.bottom < 300):
        player_surface = player_jump
    else:
        player_index += 0.2
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

screen = pygame.display.set_mode((800,400))
sky_surface = pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

# score_surface = test_font.render("My Game",False,(64,64,64))
# score_rectangle = score_surface.get_rect(center = (400,50))

#Obstacles
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_index = 0;
fly_surface = fly_frames[fly_index]

snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_index = 0;
snail_surface = snail_frames[snail_index]

obstacle_rectangle_list = []

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0;
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

player_surface = player_walk[player_index]
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

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer,200)
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
            obstacle_group.add(Obstacle(random.choice(['fly','snail','snail'])))
            # if randint(0,2):
            #     obstacle_rectangle_list.append(snail_surface.get_rect(midbottom = (randint(900,1100),300)))
            # else:
            #     obstacle_rectangle_list.append(fly_surface.get_rect(midbottom = (randint(900,1100),210)))
        if event.type == snail_timer and game_active:
            if snail_index == 0: snail_index = 1
            else: snail_index = 0;
            snail_surface = snail_frames[snail_index]
        if event.type == fly_timer and game_active:
            if fly_index == 0: fly_index = 1
            else: fly_index = 0;
            fly_surface = fly_frames[fly_index]
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        #Snail
        # screen.blit(snail_surface,snail_rectangle)
        # snail_rectangle.x -= 5;
        # if(snail_rectangle.right < -100):snail_rectangle.x= 800

        #Player
        # player_gravity += 1
        # playerAnimation()
        # player_rectangle.y += player_gravity
        # if player_rectangle.bottom >= 300: player_rectangle.bottom = 300
        # screen.blit(player_surface,player_rectangle)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        #Obstacle Movemenet
        obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        #Collision
        game_active = collision_sprite()        
        # game_active = collisions(player_rectangle,obstacle_rectangle_list)
    
        score = int(pygame.time.get_ticks() / 1000) - gameTime
        displayScore()
        
    else:
        obstacle_rectangle_list.clear()
        screen.fill((94,129,162))
        player_rectangle.midbottom = (50,300)
        player_gravity = 0;
        screen.blit(instruct_surface,instruct_rectangle)
        screen.blit(player_stand,player_stand_rectangle)
        updateScore();


    
    pygame.display.update()
    clock.tick(60)