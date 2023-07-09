import random
import pygame
from sys import exit
pygame.init()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/ysps.ttf',50)
game_active = False
gameTime = 0
bg_music = pygame.mixer.Sound("audio/bg_music.wav")
global score;
score = 0;

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphic/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphic/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0;
        self.player_jump = pygame.image.load("graphic/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0;

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            self.jump_sound.set_volume(0.25)
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
            fly_frame_1 = pygame.image.load('graphic/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphic/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            fly_index = 0;
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load("graphic/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphic/snail/snail2.png").convert_alpha()
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

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

screen = pygame.display.set_mode((800,400))
sky_surface = pygame.image.load("graphic/Sky.png").convert_alpha()
ground_surface = pygame.image.load('graphic/Ground.png').convert_alpha()

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Intro Screen
player_stand = pygame.image.load("graphic/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(center = (400,150))
bg_music.play(loops = -1)
bg_music.set_volume(0.13)

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
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                gameTime = int(pygame.time.get_ticks() / 1000)
        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacle(random.choice(['fly','snail','snail'])))
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        #Player Update
        player.draw(screen)
        player.update()

        #Obstacle Update
        obstacle_group.draw(screen)
        obstacle_group.update()

        #Collision
        game_active = collision_sprite()        

        #Score
        score = int(pygame.time.get_ticks() / 1000) - gameTime
        displayScore()
    else:
        screen.fill((94,129,162))
        screen.blit(instruct_surface,instruct_rectangle)
        screen.blit(player_stand,player_stand_rectangle)
        updateScore();


    
    pygame.display.update()
    clock.tick(60)