import pygame
from const import MIDNIGHT_BLUE, SKY_BLUE, YELLOW, JET_BLACK
from .text import Text

class Button:
    def __init__(self,surface, position=None, width=150, height=50, color=MIDNIGHT_BLUE, hover_color=SKY_BLUE, text_color=YELLOW, shadow_color=JET_BLACK, shadow_offset=5, border_radius=10, text=""):
        self.surface = surface
        self.position = position
        self.width = width
        self.height = height
        self.text = text
        self.bg_color = color
        self.text_color = text_color
        self.hover_color = hover_color
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.border_radius = border_radius
        
        self.button_text = Text(surface=self.surface, font_size=26, color=self.text_color)
        
    def render(self):
        mouse_pos = pygame.mouse.get_pos()
        button_rect =  pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        
        # Shadow
        shadow_rect = pygame.Rect(self.position.x + self.shadow_offset, self.position.y + self.shadow_offset, self.width, self.height)
        
        pygame.draw.rect(self.surface, self.shadow_color, shadow_rect, border_radius=self.border_radius)
        
        if Button.is_mouse_over(mouse_pos, button_rect):
            pygame.draw.rect(self.surface, self.hover_color, button_rect, border_radius=self.border_radius)
            
        else:
            pygame.draw.rect(self.surface, self.bg_color,button_rect, border_radius=self.border_radius)
            
        center = (self.position.x + self.width // 2, self.position.y + self.height // 2)
        self.button_text.render(self.text, center=center)
        
        return button_rect
        
    @staticmethod
    def is_mouse_over(mouse_pos,rect):
        return rect.collidepoint(mouse_pos)