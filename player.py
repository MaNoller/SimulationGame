import pygame
from settings import *
from entities import Entity

class Player(Entity):   #Just for debugging purposes,
    def __init__(self,pos,groups, obstacle_sprites, player_attack, player_enemy_interaction,debug):
        super().__init__(pos,groups,obstacle_sprites,debug)
        self.debug=debug
        self.image = pygame.image.load('graphics/player/down/down_0.png').convert_alpha() # load initial frame
        if self.debug ==True:
            self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft=pos) # create rect
        self.collision_rect = self.rect.inflate(0,Colliderect_offset['player']) # create collision rect
        self.line_of_sight = 'down' # orientation
        self.get_animation_images() # import images
        #stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.health = self.stats['health']
        self.energy= self.stats['energy']

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
        self.attacking = False
        self.attack_enable = True
        self.move_enable = True
        #weapons
        self.weapon_index = 0
        self.weapon_switch_enable= True
        self.weapon_switch_time= None
        self.weapon_switch_duration = 500
        self.player_attack = player_attack
        self.player_enemy_interaction = player_enemy_interaction
        self.damage = 20
        self.collision_rect=self.rect


    def input(self): # player inputs
        keys = pygame.key.get_pressed() # check for input
        if keys[pygame.K_UP]: # walk up
            self.direction.y = -1
            self.line_of_sight = 'up'

        elif keys[pygame.K_DOWN]: # walk down
            self.direction.y = 1
            self.line_of_sight= 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]: # walk right
            self.direction.x = 1
            self.line_of_sight = 'right'
        elif keys[pygame.K_LEFT]: # walk left
            self.direction.x = -1
            self.line_of_sight = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.attack_enable == True: # sttack
            self.attacking = True
            self.player_attack()
            self.player_enemy_interaction()

        if keys[pygame.K_e] and self.weapon_switch_enable ==True: # switch weapon
            self.weapon_switch_enable =False
            self.weapon_switch_time= pygame.time.get_ticks()
            self.weapon_index +=1
            if self.weapon_index >= 5:
                self.weapon_index = 0


        self.animation_state = 'idle'
        if True in keys: # leave idle state
            if self.attacking:
                self.animation_state = 'attacking'
            else:
                self.animation_state = 'walking'


    def weapon_switch_timer(self): # timer between weapon switches
        current_time= pygame.time.get_ticks()
        if (current_time - self.weapon_switch_time) >= self.weapon_switch_duration:
            self.weapon_switch_enable = True



    def update(self): # update player
        self.input() # input check
        self.move(self.speed) # move player
        #self.animate()
        if self.weapon_switch_enable == False:
            self.weapon_switch_timer()

    def check_death(self): # check for death
        if self.health <= 0:
            self.kill()

