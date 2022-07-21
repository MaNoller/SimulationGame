import pygame
from settings import *

class PlayerAttack(pygame.sprite.Sprite): # attack Class
    def __init__(self,groups,player):
        super().__init__(groups)
        self.line_of_sight = player.line_of_sight
        self.weapon_index = player.weapon_index
        self.player=player
        self.frame_index = 0
        self.animation_speed = 0.15
        self.get_weapon_sprite()


    def change_animation_state(self): # go through weapon/attackanimation frames, playerspecific
        self.frame_index += self.animation_speed
        if self.frame_index >= 1:
            self.kill()

    def update(self): # update fcn
        self.change_animation_state()


    def get_weapon_sprite(self): # import weapon sprite images
        self.image= pygame.image.load(f'{weapon_base_dir}{weapon_list[self.weapon_index]}/{self.line_of_sight}.png').convert_alpha()
        self.get_attack_pos()


    def get_attack_pos(self): # get weapon image according to orientation
        if self.line_of_sight == 'right':
            self.rect = self.image.get_rect(midleft = self.player.rect.midright+ pygame.math.Vector2(0,16))
        elif self.line_of_sight == 'left':
            self.rect = self.image.get_rect(midright=self.player.rect.midleft + pygame.math.Vector2(0, 16))
        elif self.line_of_sight == 'down':
            self.rect = self.image.get_rect(midtop = self.player.rect.midbottom+ pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom=self.player.rect.midtop + pygame.math.Vector2(-10, 0))