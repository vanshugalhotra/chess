import pygame
from utils import Position
from .components import Text, Clock, Banner, PlayerCard, CircularText, Button, MoveList
from const import WIDTH, JET_BLACK, WHITE, RED

class RightPanel:
    def __init__(self, surface, player1, player2, winner):
        self.padding_left = 20
        self.surface = surface
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        
        # ------------------------------------for player 1
        card1_x = WIDTH + self.padding_left
        card1_y = 20
        card1_pos = Position(card1_x, card1_y)
        card1_clock_props = {'align': 'right', 'bg_color': WHITE, 'text_color': (255, 0, 0)}
        
        self.card_1 = PlayerCard(surface=surface, padding_left=self.padding_left, position=card1_pos, player=player1, clock_props=card1_clock_props)
        
        # ------------------------------------for player 2
        card2_x = card1_x + self.card_1.width + self.card_1.padding
        card2_pos = Position(card2_x, card1_y)
        card2_clock_props = {'align': 'left', 'bg_color': JET_BLACK, 'text_color': WHITE}
        
        self.card_2 = PlayerCard(surface=surface, padding_left=self.padding_left, position=card2_pos, player=player2, clock_props=card2_clock_props)
        
        
        # ---------------------------------------play Button
        play_btn_width = 150
        play_btn_height = 50
        
        play_x = (self.card_1.position.x + self.card_1.width + self.card_2.position.x) // 2 - play_btn_width // 2
        
        play_y = self.card_1.position.y + self.card_1.height // 2 - play_btn_height // 2 + 20
        play_button_position = Position(play_x, play_y)
        
        self.play_button = Button(surface=self.surface, position=play_button_position, width=play_btn_width, height=play_btn_height, text="PLAY")
        
        #------------------------------------------winner Banner
        banner_x = 0
        banner_y = self.card_1.position.y + self.card_1.height + 10
        
        banner_position = Position(banner_x, banner_y)
        
        self.winner_banner = Banner(surface=self.surface, width=self.card_1.width, position=banner_position, text="Winner!")
        
        # --------------------------------------------material indicator
        radius = 15
        circle_x = 0
        circle_y = self.card_1.position.y + self.card_1.height - radius + 20
        circle_position = Position(circle_x, circle_y)
        
        self.material_indicator = CircularText(surface=self.surface, radius=radius, position=circle_position)
        
        
        # ----------------------------------------------- move list
        move_list_x = WIDTH + self.padding_left
        move_list_y = 310
        move_list_position = Position(move_list_x, move_list_y)
        
        self.move_list = MoveList(surface=self.surface, width=self.card_1.width + 100, position=move_list_position)
        
        
    def render(self, player1, player2, winner, material, move_list, scroll_y):
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        
        self.card_1.render(player=self.player1)
        self.card_2.render(player=self.player2)
        button_rect = self.play_button.render()
        
        show = True if self.winner else False
        pos_x = self.card_1.position.x if self.winner == self.player2 else self.card_2.position.x
        
        self.winner_banner.render(show=show, pos_x=pos_x)
        
        material_count = abs(material[0] - material[1])
        if material_count != 0:
            material_text = f'+{material_count}'
            if material[0] > material[1]: # white has more material
                pos_x = self.card_1.position.x + self.card_1.width
            elif material[1] > material[0]:
                pos_x = self.card_2.position.x + self.card_2.width
            
            self.material_indicator.render(material_text, pos_x)
            
        if len(move_list) > 0:
            self.move_list.render(move_list, scroll_y=scroll_y)
        
        return button_rect