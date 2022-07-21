from settings import *
from entities import Entity
from attack_animation import *
from math import sin, inf
from random import randint, choice




class Enemy(Entity):
    def __init__(self,pos,groups,obstacle_sprites,visible_sprites,attackable_sprites,plant_sprites,possible_positions,group_dict,dict_data,enemy_number= 'None',is_new=False):
        super().__init__(pos,groups,obstacle_sprites,dict_data =dict_data,enemy_number=enemy_number)
        #Enemy Type
        self.dict_data=dict_data # Enemy/attack combination
        self.looks = self.dict_data[0]
        self.attack_move = self.dict_data[1]
        self.enemy_number = enemy_number # Enemy number for initial setup

        self.enemy_type = enemy_dict[tuple(self.dict_data)] # Enemy Type
        self.enemy_name = enemy_dict[tuple(self.dict_data)][0] # Enemy Name

        self.image = pygame.image.load(f'graphics/monsters/{self.enemy_type[0]}/idle/0.png').convert_alpha() # Import Enemy image

        # Enemy Data
        self.damage = self.enemy_type[3]['damage']
        self.health = self.enemy_type[3]['health']
        self.resistance = self.enemy_type[3]['resistance']
        self.energy = self.enemy_type[3]['energy']


        self.enemy_type[5] +=1 #Entity counter
        if self.enemy_type[5] > self.enemy_type[6]:
            self.enemy_type[6] = self.enemy_type[5] # Set max entity number

        self.group_dict=group_dict
        self.display_surface = pygame.display.get_surface() # Set surface
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE) # Font setup
        self.attack_enable = True # entity can attack
        self.rect = self.image.get_rect(topleft=pos) # Set rect
        self.visible_sprites=visible_sprites
        self.move_enable = True # maveable

        if self.enemy_type != '392': # Different rect for bigger enemy Class
            self.collision_rect = self.rect.inflate(0, Colliderect_offset['enemy'])
        else:
            self.collision_rect = self.rect.inflate(0, Colliderect_offset['object'])

        self.line_of_sight = 'down'
        self.get_animation_images() # Get images of entity
        self.sprite_type= 'enemy'

        # attack timer
        self.attack_time= None
        self.attack_duration = 500
        self.vulnerable = True
        self.vulnerablility_time= None
        self.invulnerability_duration=500
        self.speed = 2

        #timer for random walk
        self.random_time= None
        self.random_duration=1000
        self.rand_walking= False
        self.nearest_sprite=None
        self.attackable_sprites=attackable_sprites
        self.neighbourhood_timer=None
        self.check_neighbourhood = True
        self.check_neighbourhood_duration=500
        self.target = self.attackable_sprites
        self.targetfcn = self.check_nearest_sprite # Set target (class specific)
        self.is_attacked = False

        self.possible_positions=possible_positions
        self.plant_sprites=plant_sprites

    def update(self):
        self.animate() # Animation
        if len(self.groups()):
            self.enemy_else_interaction(self.targetfcn) # walk towards/attack entity
        self.spawn_new_population()

        if self.vulnerable==False:
            self.vulnerability_timer() # Invulnerable after attack
            self.invulnerability_blink() # blinking while invulnerable
        else:
            self.image.set_alpha(255)


    def attack(self,enemy):
        stat = enemy.get_damage(self) # Enemy gets damage
        if stat == 'killed':
            if self.check_units() ==True:
                self.random_enemy_spawn(self) # Spawn own instance after a kill
        AttackAnimation([self.visible_sprites],self.dict_data,self.enemy_number,enemy.rect.center,) # Animate attack

    def check_units(self): # check if less than threshold
        if (self.enemy_type[5] <= self.enemy_type[8]) :
            return True
        else:
            return False

    def spawn_new_population(self): # create new instance of own class
        if self.enemy_type[5]< self.enemy_type[7] and self.enemy_type[9]==False: # check if less than threshold
            self.enemy_type[9] = True
            self.spawn_new_enemies()

    def create_new_enemy_class(self): # create new random enemy type
        new_enemy=[choice(enemy_name_list),choice(attack_list)]
        if tuple(new_enemy) not in self.group_dict.keys():
            self.add_to_enemy_dict(new_enemy)
            self.group_dict[tuple(new_enemy)]=pygame.sprite.Group()
        return new_enemy

    def add_to_enemy_dict(self,new_enemy): # add new enemy type to enemy dict
        enemy_dict[tuple(new_enemy)]=[new_enemy[0],150,80,{'energy':35,'resistance':30,'health':50,'damage':15,'path': f'graphics/particles/attacks/{new_enemy[1]}',
                             'death': f'graphics/particles/deaths/{death_dict[new_enemy[0]]}'},15,0,0,5,10,False]


    def spawn_new_enemies(self): # spawn 5 enemies of new class
        new_enemy=self.create_new_enemy_class()
        for i in range(0,5):
            self.random_enemy_spawn(self,new_enemy)

    def attack_timer(self): # attack cooldown
        current_time = pygame.time.get_ticks()
        if (current_time - self.attack_time) >= self.attack_duration:
            self.attack_enable = True

    def get_damage(self,player): # entity gets damage from Unit/Player/etc
        if self.vulnerable == True:
            self.vulnerablility_time = pygame.time.get_ticks()
            self.health -= player.damage
            self.vulnerable =False
            self.is_attacked = True
            enemy_state, enemy_class = self.check_death(player) # is attacked entity dead?
            if enemy_state =='killed':
                player.is_attacked = False
                #respawn
            self.setback(player)
            return enemy_state

    def vulnerability_timer(self): # vulnerability timer
        current_time = pygame.time.get_ticks()
        if (current_time-self.vulnerablility_time) >= self.invulnerability_duration:
            self.vulnerable = True

    def random_timer(self): # timer for random walking intervalls
        current_time = pygame.time.get_ticks()
        if (current_time - self.random_time) >= self.random_duration:
            self.rand_walking = False

    def check_death(self,player): #check is self is alive
        if self.health <= 0:
            DeathAnimation([self.visible_sprites],self.dict_data,self.enemy_number,self.rect.center) # play death animation
            self.kill()
            self.enemy_type[5] -= 1
            return 'killed',self.__class__.__name__
        return 'alive',self.__class__.__name__

    def setback(self,player): # knockback after attack
        dist,self.direction =self.get_distance(self.collision_rect.center, player.collision_rect.center)
        self.direction = self.direction.normalize().rotate(180)
        self.move((100-self.resistance))


    def blink(self): # blink after getting attacked
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def invulnerability_blink(self):
        self.image.set_alpha(self.blink())


    def check_nearest_sprite(self,sprites): # check nearest attackable sprite
        closest= [None,500000,None]
        for sprite in sprites:
            if self.groups()[len(self.groups())-1] != sprite.groups()[len(sprite.groups())-1]:
                SelfCollRectCenter =self.collision_rect.center
                SpriteCollRectCenter=sprite.collision_rect.center
                if SelfCollRectCenter != SpriteCollRectCenter: #check for all viable sprites, choose closest Enemy
                    distance,direction = self.get_distance(SelfCollRectCenter,SpriteCollRectCenter)
                    if distance < closest[1]:
                        closest[0] = sprite
                        closest[1] = distance
                        closest[2] = direction
        return closest # return nearest sprite, distance and direction

    ######################################################  Tried for multiprocessing -> far slower than usual
    # def get_sprite_dist_data(self,sprite,dict,i):
    #     closest=[]
    #     if self.groups()[len(self.groups()) - 1] != sprite.groups()[len(sprite.groups()) - 1]:
    #         SelfCollRectCenter = self.collision_rect.center
    #         SpriteCollRectCenter = sprite.collision_rect.center
    #         if SelfCollRectCenter != SpriteCollRectCenter:  # check for all viable sprites, choose closest Enemy
    #             distance, direction = self.get_distance(SelfCollRectCenter, SpriteCollRectCenter)
    #             #closest.append(sprite)
    #             closest.append(distance)
    #             closest.append(direction)
    #             dict[i]= closest #mal versuchen ohne shared memory was zu erreichen! -> shared memory uses pickle -> not working w/ sprites!
    #
    #     #return[0]
    #
    # def find_min_dist_sprite(self, sprite_dict,return_dict):
    #     min_dist=99999999
    #     min_key=0
    #     for key,value in return_dict.items():
    #         if value[0] < min_dist:
    #             min_dist = value[0]
    #             min_key=key
    #     closest_sprite=[sprite_dict[min_key],return_dict[min_key][0],return_dict[min_key][1]]
    #     return closest_sprite
    #
    # def check_nearest_sprite(self,sprites):
    #     manager=multiprocessing.Manager()
    #     return_dict=manager.dict()
    #     jobs=[]
    #
    #     sprite_dict={} # sprite dict in multiprocess reingeben und ergebnis alles in ein array speichern, zahl verweißt dann auf eintrag in sprite dict!
    #     for i,sprite in enumerate(sprites):
    #         sprite_dict[i]= sprite
    #         proces =multiprocessing.Process(target=self.get_sprite_dist_data,args=[sprite,return_dict,i])
    #         jobs.append(proces)
    #         proces.start()
    #     for proc in jobs:
    #         proc.join()
    #     print('durch')
    #     closest = self.find_min_dist_sprite(sprite_dict,return_dict)
    #     return closest

 # ############################################

    def get_distance(self, SelfCollRectCenter,SpriteCollRectCenter): # get distance/direction to Entity
        sprite_pos=pygame.math.Vector2(SpriteCollRectCenter)
        own_pos=pygame.math.Vector2(SelfCollRectCenter)
        distance=(sprite_pos-own_pos).magnitude()
        if distance:
            direction = (sprite_pos-own_pos).normalize()
        return distance, direction

    def choose_target(self): # choose target function
        if self.is_attacked:
            target= self.attackable_sprites
        else:
            target=self.target
        return target

    def enemy_else_interaction(self,targetfcn): #what is entity doig?
        target= self.choose_target()
        if self.check_neighbourhood ==True: # check for nearby entities
            self.neighbourhood_time = pygame.time.get_ticks()
            self.check_neighbourhood = False
            self.nearest_sprite, self.distance, self.direction = targetfcn(target)
            if self.direction == None:
                self.rand_walking = False
        self.check_neighbourhood_timer()
        if self.distance < self.enemy_type[1]: # entity in reach
            self.rand_walking = False
            if self.distance < self.enemy_type[2] and self.attack_enable == True: # in attack range
                self.attack_time = pygame.time.get_ticks()
                self.attack_success(self.attack) #attack
                self.attack_enable = False
            else:
                if self.attack_enable == False:
                    self.attack_timer()
                self.move(self.speed) # move towards entity
        else:
            if self.rand_walking == False:
                self.direction = self.random_walk()  # random walking
                self.random_time = pygame.time.get_ticks()
                self.rand_walking = True
            self.move(self.speed)
            self.random_timer()

    def check_neighbourhood_timer(self): # not checking in every frame, timer
        current_time = pygame.time.get_ticks()
        if (current_time - self.neighbourhood_time) >= self.check_neighbourhood_duration:
            self.check_neighbourhood = True



    def attack_success(self,attack): # attacks have a success rate
        rate=randint(0,10)
        if rate >= 4:
            attack(self.nearest_sprite)

    def random_enemy_spawn(self,player,new=False): #spawn enemies at random places
        x,y = choice(self.possible_positions) #random pos
        if new: #new enemy class?
            dict_input=tuple(new)
            dict_data=new
        else:
            dict_input=tuple(player.dict_data)
            dict_data=player.dict_data
        if player.__class__.__name__ == 'Enemy': #Enemy Class
            Enemy((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites,self.group_dict[dict_input]],
                  self.obstacle_sprites, self.visible_sprites, self.attackable_sprites,self.plant_sprites,
                  self.possible_positions,self.group_dict,dict_data,enemy_number='393')
        elif player.__class__.__name__ == 'Prey': # Prey Class
            Prey((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites,self.group_dict[dict_input]],
                 self.obstacle_sprites, self.visible_sprites, self.attackable_sprites, self.plant_sprites,
                 self.possible_positions,self.group_dict,dict_data, enemy_number='390')



class Prey(Enemy): #Prey Class
    def __init__(self,pos,groups,obstacle_sprites,visible_sprites,attackable_sprites,plant_sprites,possible_positions,group_dict,dict_data,enemy_number= 'None'):
        super().__init__(pos,groups,obstacle_sprites,visible_sprites,attackable_sprites,plant_sprites,possible_positions,group_dict,dict_data,enemy_number=enemy_number)
        self.plant_sprites=plant_sprites
        self.target = self.plant_sprites # different default target fcn





