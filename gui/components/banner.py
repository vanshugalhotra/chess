import pygame
from const import AMBER, WHITE
from .text import Text


class Banner:
    def __init__(self,surface, width=0, height=40, text="", color=AMBER, text_color=WHITE, position=None):
        self.width = width       
        self.height = height
        self.bg_color = color
        self.text_color = text_color
        self.position = position
        self.surface = surface
        self.text = text
        self.banner_text = Text(surface=self.surface, font_size=24)
        
    def render(self, show, pos_x):
        self.position.x = pos_x
        if show:
            banner_rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
            
            pygame.draw.rect(self.surface, self.bg_color, banner_rect, border_radius=8) 
            
            center = (self.position.x + self.width // 2, self.position.y + self.height // 2)
            
            self.banner_text.render(self.text, center=center)