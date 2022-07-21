WIDTH=1280
HEIGHT=720
FPS=60
TILESIZE=64

#directions
player_base_dir = 'graphics/player/'
enemy_base_dir='graphics/monsters/'
weapon_base_dir='graphics/weapons/'

#offsets for sprites
Colliderect_offset={
    'player': -40,
    'object': -50,
    'grass':-15,
    'boundary': -5,
    'enemy': -20
}


enemy_name_list = ['bamboo', 'spirit',  'squid'] # possible enemy types
attack_list=['leaf_attack','thunder','slash','claw'] # possible attacks
death_dict={                             # Death animations for each enemy type
    'bamboo':'bamboo',
    'spirit':'nova',
    'squid':'smoke_orange'
}


enemy_dict={    # start enemy dict
    tuple(['bamboo','leaf_attack']):['bamboo',150,80,{'energy':35,'resistance':30,'health':5,'damage':15,'path':'graphics/particles/attacks/leaf_attack',
                             'death':'graphics/particles/deaths/bamboo'},15,0,0,5,10,False],
    tuple(['spirit','thunder']):['spirit',150,80,{'energy':35,'resistance':30,'health':50,'damage':15,'path':'graphics/particles/attacks/thunder',
                             'death':'graphics/particles/deaths/nova'},15,0,0,5,10,False],
    tuple(['squid','slash']):['squid',150,80,{'energy':35,'resistance':30,'health':50,'damage':15,'path':'graphics/particles/attacks/slash',
                             'death':'graphics/particles/deaths/smoke_orange'},15,0,0,5,10,False],
}


weapon_list=[ # weapon list, was used for player, remainder of "Game" -> unused
    'axe',
    'lance',
    'rapier',
    'sai',
    'sword',
]


# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'

ENEMY_BAR_HEIGHT = 5
ENEMY_HEALTH_BAR_WIDTH = 50
ENEMY_ENERGY_BAR_WIDTH = 35