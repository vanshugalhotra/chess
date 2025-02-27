import pygame
from const import BROWN, JET_BLACK, WIDTH_OFFSET
from .text import Text
from .clock import Clock
from utils import Position


class PlayerCard: 
    def __init__(self, surface, width=180, height=220, image_size=170, padding_left=0, position=None, color = BROWN, shadow_color=JET_BLACK, player=None, clock_props={}):
        self.width = width
        self.height = height
        self.image_size = image_size
        self.padding = (WIDTH_OFFSET - 2*(self.width + padding_left))
        self.position = position
        
        self.color = color
        self.shadow_offset = 8
        self.shadow_color = shadow_color
        self.border_radius = 15
        
        self.surface = surface
        
        self.player = player
        
        self.player_text = Text(surface=self.surface)
        
        if clock_props['align'] == 'right':
            clock_offset_x = self.width - 20
        else:
            clock_offset_x = -150
        clock_x = self.position.x + clock_offset_x
        clock_y = self.position.y + 10
        player_clock_pos = Position(clock_x, clock_y)
        
        self.player_clock = Clock(surface=self.surface, time=self.player.time, align=clock_props['align'],bg_color=clock_props['bg_color'], text_color=clock_props['text_color'], position=player_clock_pos)
        
    def render(self, player):
        self.player = player
        
        shadow_rect = pygame.Rect(self.position.x + self.shadow_offset, self.position.y + self.shadow_offset, self.width, self.height)
        
        pygame.draw.rect(self.surface, self.shadow_color, shadow_rect, border_radius=self.border_radius)
        
        # loading and scaling player image 
        player_img = pygame.image.load(self.player.image)
        player_img = pygame.transform.scale(player_img,(self.image_size, self.image_size))
        
        # creating the card BACKGROUND
        card_rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(self.surface, self.color, card_rect, border_radius=self.border_radius)
        
        # blitting the card image
        self.surface.blit(player_img, (self.position.x, self.position.y))
        
        # rendering player's name
        coords = (self.position.x + self.width // 2, self.position.y + self.image_size + 30)
        
        self.player_text.render(self.player.name, center=coords) 
        
        # rendering the player's Clock
        self.player_clock.render(time=self.player.time)       
    