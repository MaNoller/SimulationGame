import pygame
from settings import *


class WorldObject(pygame.sprite.Sprite): # ObjectClass
    def __init__(self, pos, groups, sprite_type,nodes, img_surf = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.x_pos, self.y_pos = pos
        self.nodes=nodes
        self.image=img_surf
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = self.rect.inflate(0,Colliderect_offset[sprite_type])

    def add_node(self):
        self.nodes[int(self.pos[1] / TILESIZE)][int(self.pos[0] / TILESIZE)] = 1

class Grass(WorldObject): # Grass Class
    def __init__(self, pos, groups, sprite_type, obstacle_sprites,nodes, img_surf = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(pos, groups, sprite_type, nodes,img_surf = pygame.Surface((TILESIZE,TILESIZE)))
        self.health = 0
        self.enemy_number = None
        self.image = img_surf
        self.vulnerable = True
        self.obstacle_sprites=obstacle_sprites
        self.pos=pos


    def check_collision_on_spawn(self): # check if there is already sth on spawn pos
        for sprite in self.obstacle_sprites:
            if self.collision_rect.center != sprite.collision_rect.center:# and self.collision_rect.colliderect(sprite.rect):
                if self.collision_rect.colliderect(sprite.collision_rect): # if there is sth on pos:
                    self.kill()             # destroy self
                    return 'killed'

    def get_damage(self,enemy):
        self.kill() # destroy entity on damage
        return 'killed'

