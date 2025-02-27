import pygame
from const import WHITE, LIGHT_GRAY
from .text import Text
from utils import Position
from .scrollbar import ScrollBar


class MoveList:
    def __init__(self, surface, width=0, height=270, position=None, bg_color=(35, 32, 30), highlight_color_1 = (60, 57, 54), highlight_color_2 = (45, 42, 40), scrollbar_color = LIGHT_GRAY, text_color = WHITE):
        self.surface = surface
        self.width = width
        self.height = height
        self.position = position
        
        self.row_height = 30
        
        self.bg_color = bg_color
        self.highlight_color_1 = highlight_color_1
        self.highlight_color_2 = highlight_color_2
        self.scrollbar_color = scrollbar_color
        self.text_color = text_color
        
        self.scroll_y = 0
        self.max_scroll = 0
        
        self.move_text = Text(surface=self.surface, font_size=22, color=self.text_color)
        
        self.move_list = []
        
        scroll_pos_x = self.position.x + self.width - 10
        scroll_pos_y = self.position.y
    
        scroll_pos = Position(scroll_pos_x, scroll_pos_y)
        
        self.scrollbar = ScrollBar(surface=self.surface, position=scroll_pos, height=self.height, scroll_y=self.scroll_y, color=self.scrollbar_color, max_scroll=self.max_scroll)
        
        
    def render(self, move_list, scroll_y):
        self.scroll_y = scroll_y
        self.move_list = move_list
        self.max_scroll = max(0, len(move_list) * self.row_height - self.height)
        
        self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
        
        move_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.move_text.surface = move_surface
        
        # BACKGROUND
        pygame.draw.rect(self.surface, self.bg_color, (self.position.x, self.position.y, self.width, self.height), border_radius=10)
        
        # rendering each Move
        for i in range(0, len(move_list), 2):
            white_move = move_list[i]
            black_move = move_list[i+1] if i+1 < len(move_list) else ""
            
            row_y = i // 2 * self.row_height - self.scroll_y
            if self.position.y <= row_y + self.position.y < self.position.y + self.height:
                # setting color alternating
                white_move_color = self.highlight_color_1 if i%4 == 0 else self.highlight_color_2
                black_move_color = self.highlight_color_2 if i%4 == 0 else self.highlight_color_1
                
                pygame.draw.rect(move_surface, white_move_color,(0, row_y, self.width // 2, self.height) )
                
                pygame.draw.rect(move_surface, black_move_color, (self.width // 2, row_y, self.width // 2, self.height))
                
                # rendering move text
                self.move_text.render(f"{i//2 + 1}", left=10, top=row_y)
                self.move_text.render(white_move, left=40, top=row_y)
                self.move_text.render(black_move, left=self.width // 2 + 10, top=row_y)
        
        self.surface.blit(move_surface, (self.position.x, self.position.y))
        
        self.scrollbar.render(max_scroll=self.max_scroll, scroll_y=self.scroll_y)
