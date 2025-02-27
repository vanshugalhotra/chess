from .text import Text
from const import WHITE, RED
import pygame

class Clock:
    def __init__(self, surface, width=160, height=40, position=None, time=0, align='right', bg_color=WHITE, text_color=RED):
        self.width = width
        self.height = height
        self.surface = surface
        self.position = position
        self.bg_color = bg_color
        self.text_color = text_color
        self.timer_text = Text(surface=self.surface, font="Lucida Console", font_size=25, bold=True, color=self.text_color)
        self.clock_time = time
        self.align = align
        
    def render(self, time):
        self.clock_time = time
        clock_rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        
        pygame.draw.rect(self.surface, self.bg_color, clock_rect, border_radius=8)
        
        # rendering the clock time
        render_time = Clock.format_time(self.clock_time)
        
        if self.align == 'right':
            right = self.position.x + self.width - 10
            centery = self.position.y + self.height // 2
            self.timer_text.render(render_time, right=right, centery=centery)

        else:
            left = self.position.x + 10
            centery = self.position.y + self.height // 2
            self.timer_text.render(render_time, left=left, centery=centery)
            
    @staticmethod
    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"
