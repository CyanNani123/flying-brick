import pygame

#set dummy driver for unix
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
    
class Screen():
    def __init__(self,width=400,height=600):
        '''initialize pygame screen'''
        pygame.init
        self.screen = pygame.display.set_mode((width,height))
        self.screen.fill(pygame.Color(255,255,255))
        pygame.display.init()
        pygame.display.update()