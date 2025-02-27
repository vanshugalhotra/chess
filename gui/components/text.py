from const import WHITE
import pygame

class Text:
    def __init__(self, surface,font="Arial",font_size=22, bold=True, color=WHITE):
        self.font = pygame.font.SysFont(font, font_size, bold=bold)
        self.color = color
        self.surface = surface
        
    def render(self, text, **coords):
        render_text = self.font.render(str(text), True, self.color)
        render_rect = render_text.get_rect(**coords)
        
        self.surface.blit(render_text, render_rect)
