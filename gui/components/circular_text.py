import pygame
from const import LIGHT_GRAY, JET_BLACK
from .text import Text

class CircularText:
    def __init__(self, surface, radius=15, bg_color=LIGHT_GRAY, text_color=JET_BLACK, position=None, text=""):
        self.surface = surface
        self.radius = radius
        
        self.position = position
        self.bg_color = bg_color
        self.text_color = text_color
        self.text = text
        
        self.circle_text = Text(surface=self.surface, font_size=18, color=self.text_color)
        
    def render(self, text, pos_x):
        self.position.x = pos_x - self.radius + 10
        self.text = text
        center = (self.position.x, self.position.y)
        
        pygame.draw.circle(self.surface, self.bg_color, center , self.radius)
        
        self.circle_text.render(self.text, center=center)