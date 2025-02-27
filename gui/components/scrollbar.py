import pygame
from const import LIGHT_GRAY

class ScrollBar:
    def __init__(self, surface, position=None, height=0, max_scroll=0, color=LIGHT_GRAY, scroll_y=0):
        self.surface = surface
        self.position = position
        self.height = height
        self.max_scroll = max_scroll
        self.color = color
        self.scroll_y = scroll_y
        
    def render(self, max_scroll, scroll_y):
        self.max_scroll = max_scroll
        self.scroll_y = scroll_y
        if self.max_scroll > 0:
            scrollbar_height = self.height * (self.height / (self.height + self.max_scroll))
            
            scrollbar_y = self.position.y + (self.scroll_y / self.max_scroll) * (self.height - scrollbar_height)
            
            pygame.draw.rect(self.surface, self.color, (self.position.x, scrollbar_y, 8, scrollbar_height), border_radius=5)