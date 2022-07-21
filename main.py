import pygame, sys
from settings import *
from level import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) # Set screen
        self.clock = pygame.time.Clock() # Set clock
        pygame.display.set_caption('My Game') # Caption
        self.level = Level() # Start

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT: # Exit game
                    pygame.quit()
                    sys.exit()


            self.screen.fill('black') # Black background, as base
            self.level.run() # Run Game
            pygame.display.update() # Update
            self.clock.tick(FPS)

if __name__ == '__main__':
    game=Game()
    game.run()