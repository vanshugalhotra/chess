import pygame
from const import *


class Game:
    
    def __init__(self):
        pass
    
    
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if( (row + col) & 1 == 0 ): # if is even
                    color = LIGHT_GREEN
                else:
                    color = DARK_GREEN
                    
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
            