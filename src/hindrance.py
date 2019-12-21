import pygame

class Hindrance():
    def __init__(self, x, height, gap_y, width = 60, gap_size = 180):
        '''init hindrance object'''
        self.gap_y = gap_y
        self.x = x
        self.height = height
        self.top = pygame.Rect(self.x, 0, width, self.gap_y)
        self.bottom = pygame.Rect(self.x, self.gap_y+gap_size, width, self.height)
        self.was_passed = bool(0)
    
    def draw(self, screen):
        '''draw a hindrance on pygame screen'''
        pygame.draw.rect(screen, pygame.Color(0,150,0), self.top)
        pygame.draw.rect(screen, pygame.Color(0,150,0), self.bottom)
        
    def move_x(self,x):
        '''move hindrance in x direction'''
        self.x += x
        self.top = self.top.move(x,0)
        self.bottom = self.bottom.move(x,0)