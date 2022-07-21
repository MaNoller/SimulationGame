import pygame
from settings import *
from support import import_graphics
from os import listdir
from random import randint

class Entity(pygame.sprite.Sprite):
    def __init__(self,pos,groups, obstacle_sprites, dict_data = None, enemy_number = 'None', debug= False):
        super().__init__(groups)
        self.pos = pos
        self.obstacle_sprites = obstacle_sprites
        self.animation_speed = 0.1 # animation speed
        self.animation_index = 0 # image index for animation
        self.speed = 5 # movement speed
        self.direction = pygame.math.Vector2()
        self.animation_state = 'idle'
        self.enemy_number=enemy_number
        self.debug=debug #debug state


        if self.enemy_number != 'None':
            self.enemy_type = enemy_dict[tuple(dict_data)]
            self.health = self.enemy_type[3]['health']
            self.energy = self.enemy_type[3]['energy']



    def animate(self): #animate entity
        if self.enemy_number == 'None': # -> player?
            if self.animation_state == 'idle':
                temp_image = self.images[f'{self.line_of_sight}_{self.animation_state}']
            else:
                temp_image = self.images[self.line_of_sight]
        else:
            temp_image = self.images[self.animation_state]
        if self.animation_index >= len(temp_image):
            self.animation_index = 0
        self.image = temp_image[int(self.animation_index)]
        if self.enemy_number != 'None':
            self.bars_update()
        self.animation_index += self.animation_speed


    def get_animation_images(self): # get images for animation
        self.images={}
        if self.enemy_number == 'None':
            base_dir=player_base_dir
        else:
            base_dir= f'{enemy_base_dir}/{self.enemy_type[0]}'

        for folder in listdir(base_dir):
            self.images[folder]=[]
        for key in self.images.keys():
            self.images[key] = import_graphics(f'{base_dir}/{key}')


    def move(self, speed): # move entity
        if self.move_enable:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.collision_rect.centerx += self.direction.x * speed
            if self.debug ==True:
                pass
            else:
                self.collision(self.direction,'x')
            self.collision_rect.centery += self.direction.y * speed
            if self.debug ==True:
                pass
            else:
                self.collision(self.direction,'y')
            self.rect.center = self.collision_rect.center



    def collision(self, direction, keyword): #check for collission w/ obstacles
        if keyword =='x':
            for obstacle in self.obstacle_sprites: # x direction
                if self.collision_rect.center != obstacle.collision_rect.center:
                    if self.collision_rect.colliderect(obstacle.collision_rect):
                        if self.direction.x >0:
                            self.collision_rect.right = obstacle.collision_rect.left #no moving through
                        if self.direction.x <0:
                            self.collision_rect.left = obstacle.collision_rect.right #no moving through
        if keyword == 'y':
            for obstacle in self.obstacle_sprites: # y direction
                if self.collision_rect.center != obstacle.collision_rect.center:
                    if self.collision_rect.colliderect(obstacle.collision_rect):
                        if self.direction.y > 0:
                            self.collision_rect.bottom = obstacle.collision_rect.top #no moving through
                        if self.direction.y < 0:
                            self.collision_rect.top = obstacle.collision_rect.bottom #no moving through


    def bars_update(self): # Health bars update
        self.display_bar()


    def show_bar(self, current, max_amount, color): # show bars
        if color == HEALTH_COLOR:
            pos= (0,0)
            width=ENEMY_HEALTH_BAR_WIDTH
        else:
            pos=(0,ENEMY_BAR_HEIGHT)
            width=ENEMY_ENERGY_BAR_WIDTH
        self.health_bar_rect = pygame.Rect(pos[0], pos[1], width, ENEMY_BAR_HEIGHT)
        ratio = current / max_amount
        current_width = self.health_bar_rect.width * ratio
        current_rect = self.health_bar_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.image, UI_BG_COLOR, pygame.Rect(pos[0], pos[1], width, ENEMY_BAR_HEIGHT))
        pygame.draw.rect(self.image, color, current_rect)



    def display_bar(self):
        self.show_bar( self.health, self.enemy_type[3]['health'], HEALTH_COLOR)
        self.show_bar(self.energy, self.enemy_type[3]['energy'], ENERGY_COLOR)


    def random_walk(self): # random walking direction
        x_pos, y_pos = pygame.math.Vector2(self.rect.center).normalize()
        x_goal = x_pos + randint(-1,1)
        y_goal = y_pos + randint(-1,1)
        pos_goal=pygame.math.Vector2(x_goal,y_goal).normalize()
        return pos_goal
