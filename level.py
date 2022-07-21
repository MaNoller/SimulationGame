import multiprocessing

from settings import *
from player import Player
from support import *
from settings import enemy_name_list,attack_list
from random import choice, randint
from enemies import Enemy,Prey
from ui import UI
from weapons import PlayerAttack
from worldobject import WorldObject, Grass
import numpy as np


class Level:
    def __init__(self):
        self.debug= True # For player interaction settings
        #sprite groups
        self.visible_sprites = MovingCameraGroup() # Visible group
        self.obstacle_sprites = pygame.sprite.Group() # obstacle group
        self.attackable_sprites = pygame.sprite.Group() # Attackable group
        self.weapon_sprites = pygame.sprite.Group() # Weapon group
        self.plant_sprites=pygame.sprite.Group() # Plant group
        self.group_dict={} # dict for different combinations of enemies and attacks
        for k in range(0, 3):
            self.group_dict[tuple([enemy_name_list[k], attack_list[k]])] = pygame.sprite.Group() # starting groups

        self.map_size=None
        self.plant_positions=[] # Positions of plant sprites
        self.plant_amount= 0 # amount of plant sprites
        self.max_plants=0 # max amount of plant sprites
        self.grass= None


        self.nodes = self.create_map() # create map

        #player
        self.ui = UI() # create User Interface


    def create_map(self):
        layouts = {
            'boundary': csv_import('graphics/map/map_FloorBlocks.csv'),
            'grass': csv_import('graphics/map/map_Grass.csv'),
            'object' : csv_import('graphics/map/map_Objects.csv'),
            'entities' : csv_import('graphics/map/map_Entities.csv'),
            'map_floor':csv_import('graphics/map/map_Floor.csv')
                  }
        graphics = {
            'grass': import_graphics('graphics/grass'),
            'objects': import_graphics('graphics/objects')
        }
        row_count = sum(1 for row in layouts['entities'])
        line_count = len(layouts['entities'][0])
        nodes= np.zeros((row_count,line_count))

        for key,item in layouts.items():
            for row,row_val in enumerate(item):
                for line,line_el in enumerate(row_val):
                    if line_el != '-1':
                        x = line * TILESIZE
                        y = row * TILESIZE
                        if key == 'boundary':
                            WorldObject((x, y), [self.obstacle_sprites], key,nodes) #Boundary objects around map
                        elif key == 'grass':
                            Grass((x,y),[self.visible_sprites,self.obstacle_sprites,self.plant_sprites],key,self.obstacle_sprites,nodes,choice(graphics['grass'])) # spawn grass
                            self.plant_amount +=1
                        elif key =='object':
                            WorldObject((x, y), [self.visible_sprites,self.obstacle_sprites], key,nodes, graphics['objects'][int(line_el)]) # spawn other objects
                        elif key == 'entities':
                            if line_el =='394': #player # spawn player
                                if self.debug==True:
                                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites, self.player_attack, self.player_enemy_interaction,self.debug)
                                else:
                                    self.player = Player((x,y), [self.visible_sprites,self.obstacle_sprites], self.obstacle_sprites, self.player_attack, self.player_enemy_interaction)
                            elif line_el =='390': # spawn Prey Class
                                Prey((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites,self.group_dict[tuple([enemy_name_list[0],attack_list[0]])]],
                                      self.obstacle_sprites,self.visible_sprites,self.attackable_sprites,self.plant_sprites,self.plant_positions,self.group_dict,[enemy_name_list[0],attack_list[0] ],enemy_number=line_el)
                            else: # Spawn Enemy Class
                                Enemy((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites, self.group_dict[tuple([enemy_name_list[2],attack_list[2]])]],
                                      self.obstacle_sprites,self.visible_sprites,self.attackable_sprites,self.plant_sprites,self.plant_positions,self.group_dict,[enemy_name_list[2],attack_list[2] ],enemy_number=line_el)
                        elif key== 'map_floor': # Mapping of grass sprites
                            if line_el[:-1]=='26':
                                self.plant_positions.append((x,y))
        self.max_plants = self.plant_amount
        self.grass = graphics['grass']
        return nodes


    def player_attack(self):
        PlayerAttack([self.visible_sprites, self.weapon_sprites],self.player) # Player attack


    def player_enemy_interaction(self):
        for sprite in self.weapon_sprites: #check if weapon
            collisions= pygame.sprite.spritecollide(sprite,self.attackable_sprites, False) # collides w/ attackable sprite entitites
            if collisions:
                for target in collisions:
                    target.get_damage(self.player) # target gets damaged

    def random_plants(self): # spawn plant at random pos
        while len(self.plant_sprites) < self.max_plants: # if not max amount of plants
            x,y = choice(self.plant_positions) # choose random position
            gras_candidate = Grass((x, y), [self.visible_sprites, self.obstacle_sprites, self.plant_sprites], 'grass',
                  self.obstacle_sprites,self.nodes,choice(self.grass)) #create grass sprite at rand pos
            grass_state = gras_candidate.check_collision_on_spawn() # check if there are no other plants on that pos
            if grass_state != 'killed':
                self.plant_amount += 1



    def run(self):
        self.random_plants() # spawn plant at random pos
        p1= multiprocessing.Process(target=self.visible_sprites.draw_sprites, args=[self.player]) #in case data visals will be implemented
        p1.start()
        #self.visible_sprites.draw_sprites(self.player) # draws sprites
        self.visible_sprites.update() # update all visible sprites
        self.ui.display(self.player)


class MovingCameraGroup(pygame.sprite.Group): #Follows the player
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.x_mid = self.display_surface.get_size()[0] // 2
        self.y_mid = self.display_surface.get_size()[1] // 2


        self.bg_surf = pygame.image.load('graphics/map/ground.png').convert()
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))

    def draw_sprites(self,player):

        #offset to player sprite
        self.offset = pygame.math.Vector2()
        self.offset.x = player.rect.centerx - self.x_mid
        self.offset.y = player.rect.centery - self.y_mid

        #redraw floor
        self.bg_newpos = self.bg_rect.topleft - self.offset
        self.display_surface.blit(self.bg_surf, self.bg_newpos)

        self.ordered_sprites(self.sprites())


    def ordered_sprites(self, sprite_group): # overlap for sprites
        ordered_group = pygame.sprite.Group()
        for sprite in sorted(sprite_group, key= lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)



    def draw_bar_sprites(self,sprite_group): # draw healthbar for enemies
        for sprite in sprite_group:
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)



    def enemys_update(self,player):
        enemy_sprites = []
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type =='enemy':
                enemy_sprites.append(sprite)
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

