import pygame
from support import import_graphics
from settings import enemy_dict

class AttackAnimation(pygame.sprite.Sprite):
    def __init__(self,groups,dict_data,enemy_number,pos):
        super().__init__(groups)
        self.dict_data=dict_data
        self.pos=pos
        self.frame_index = 0
        self.animation_speed = 0.15 # attack animation speed
        self.enemy_number=enemy_number
        self.frames = import_graphics(enemy_dict[tuple(self.dict_data)][3]['path']) # get animation frames
        self.image = self.frames[int(self.frame_index)] # set initial image
        self.rect = self.image.get_rect(center=self.pos) # set rect

    def change_animation_state(self): # go through animation images
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): # if last frame used: kill animation
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]


    def update(self):
        self.change_animation_state() # update animation

class DeathAnimation(pygame.sprite.Sprite):
    def __init__(self,groups,dict_data,enemy_number,pos):
        super().__init__(groups)
        self.dict_data=dict_data
        self.pos=pos
        self.frame_index = 0
        self.animation_speed = 0.15 # attack animation speed
        self.enemy_number=enemy_number
        self.frames = import_graphics(enemy_dict[tuple(self.dict_data)][3]['death'])  # get animation frames
        self.image = self.frames[int(self.frame_index)] # set initial image
        self.rect = self.image.get_rect(center=self.pos) # set rect


    def change_animation_state(self):  # go through animation images
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): # if last frame used: kill animation
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]


    def update(self):
        self.change_animation_state()
