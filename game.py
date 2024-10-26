import pygame
from const import *
from board import Board
from config import Config
from square import Square
from dragger import Dragger
from piece import Piece
from player import Player
import time
from sound import Sound
import os

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class TextComponent:
    def __init__(self, surface,font="Arial",font_size=22, bold=True, color=(255, 255, 255)):
        self.font = pygame.font.SysFont(font, font_size, bold=bold)
        self.color = color
        self.surface = surface
        
    def render(self, text, **coords):
        render_text = self.font.render(str(text), True, self.color)
        render_rect = render_text.get_rect(**coords)
        
        self.surface.blit(render_text, render_rect)

class Clock:
    def __init__(self, surface, width=160, height=40, position=None, time=0, align='right', bg_color=(255, 255, 255), text_color=(255,0,0)):
        self.width = width
        self.height = height
        self.surface = surface
        self.position = position
        self.bg_color = bg_color
        self.text_color = text_color
        self.timer_text = TextComponent(surface=self.surface, font="Lucida Console", font_size=25, bold=True, color=self.text_color)
        self.clock_time = time
        self.align = align
        
    def render(self, time):
        self.clock_time = time
        clock_rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        
        pygame.draw.rect(self.surface, self.bg_color, clock_rect, border_radius=8)
        
        # rendering the clock time
        render_time = Game.format_time(self.clock_time)
        
        if self.align == 'right':
            right = self.position.x + self.width - 10
            centery = self.position.y + self.height // 2
            self.timer_text.render(render_time, right=right, centery=centery)

        else:
            left = self.position.x + 10
            centery = self.position.y + self.height // 2
            self.timer_text.render(render_time, left=left, centery=centery)
            
class PlayerCard: 
    def __init__(self, surface, width=180, height=220, image_size=170, padding_left=0, position=None, color = (50, 45, 42), shadow_color=(30, 30, 30), player=None, clock_props={}):
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
        
        self.player_text = TextComponent(surface=self.surface)
        
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
        
class Banner:
    def __init__(self,surface, width=0, height=40, color='#f39c12', text_color="#ffffff", position=None):
        self.width = width       
        self.height = height
        self.bg_color = color
        self.text_color = text_color
        self.position = position
        self.surface = surface
        
        self.banner_text = TextComponent(surface=self.surface, font_size=24)
        
    def render(self, show, pos_x):
        self.position.x = pos_x
        if show:
            banner_rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
            
            pygame.draw.rect(self.surface, self.bg_color, banner_rect, border_radius=8) 
            
            center = (self.position.x + self.width // 2, self.position.y + self.height // 2)
            
            self.banner_text.render("Winner!!", center=center)

class Button:
    def __init__(self,surface, position=None, width=150, height=50, color=(44, 62, 80), hover_color=(52, 152, 219), text_color=(241, 196, 15), shadow_color=(30, 30, 30), shadow_offset=5, border_radius=10, text=""):
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
        
        self.button_text = TextComponent(surface=self.surface, font_size=26, color=self.text_color)
        
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
        
class CircularText:
    def __init__(self, surface, radius=15, bg_color=(240, 240, 240), text_color=(0,0,0), position=None, text=""):
        self.surface = surface
        self.radius = radius
        
        self.position = position
        self.bg_color = bg_color
        self.text_color = text_color
        self.text = text
        
        self.circle_text = TextComponent(surface=self.surface, font_size=18, color=self.text_color)
        
    def render(self, text, pos_x):
        self.position.x = pos_x - self.radius + 10
        self.text = text
        center = (self.position.x, self.position.y)
        
        pygame.draw.circle(self.surface, self.bg_color, center , self.radius)
        
        self.circle_text.render(self.text, center=center)

class ScrollBar:
    def __init__(self, surface, position=None, height=0, max_scroll=0, color=(100, 100, 100), scroll_y=0):
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
            
class MoveList:
    def __init__(self, surface, width=0, height=270, position=None, bg_color=(35, 32, 30), highlight_color_1 = (60, 57, 54), highlight_color_2 = (45, 42, 40), scrollbar_color = (100, 100, 100), text_color = (255, 255, 255)):
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
        
        self.move_text = TextComponent(surface=self.surface, font_size=22, color=self.text_color)
        
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

class RightUI:
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
        card1_clock_props = {'align': 'right', 'bg_color': (255, 255, 255), 'text_color': (255, 0, 0)}
        
        self.card_1 = PlayerCard(surface=surface, padding_left=self.padding_left, position=card1_pos, player=player1, clock_props=card1_clock_props)
        
        # ------------------------------------for player 2
        card2_x = card1_x + self.card_1.width + self.card_1.padding
        card2_pos = Position(card2_x, card1_y)
        card2_clock_props = {'align': 'left', 'bg_color': (30, 30, 30), 'text_color': (255, 255, 255)}
        
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
        
        self.winner_banner = Banner(surface=self.surface, width=self.card_1.width, position=banner_position)
        
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
        
class Game:
    
    def __init__(self, surface):
        self.hovered_sqr = None
        self.constants = Constants()
        self.board = Board(self.constants)
        self.dragger = Dragger()
        self.config = Config()
        
        self.surface = surface
        
        self.start = False
        self.engine_mode = False
        
        initial_time = 600
        
        self.white = Player("Vanshu Galhotra", "me.png", initial_time=initial_time)
        self.player2 = Player("Prem Pal", "prem.png", initial_time=initial_time)
        self.black = self.player2
        self.engine = Player("Ustaad Ji", "ustaad.png", initial_time=initial_time)
        self.current_player = self.white
        
        self.winner = None
        
        self.scroll_y = 0
        
        self.right_side = RightUI(surface=self.surface, player1=self.white, player2=self.black, winner=self.winner)
        
    # render methods
    def show_bg(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if ((row + col) & 1 == 0) else theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                
                # row coordinates
                if col == 0:
                    color = theme.bg.dark if (row % 2 == 0) else theme.bg.light
                    
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5+row*SQSIZE)
                    
                    #blit
                    surface.blit(lbl, lbl_pos)
                
                # col coordinates
                if row == 7:
                    color = theme.bg.dark if ( (row + col) % 2 == 0) else theme.bg.light 
                    
                    
                    # label
                    lbl = self.config.font.render(Square.get_alphacode(col), 1, color)
                    lbl_pos = (col*SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    
                    
                    #blit
                    surface.blit(lbl, lbl_pos)
                    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece(): # if we have a piece on a particular square
                    piece = self.board.squares[row][col].piece
                    # all pieces except the dragging one
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture) # getting image path into image object
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2 # centering the image
                        piece.texture_rect = img.get_rect(center=img_center) # coordinates
                        surface.blit(img, piece.texture_rect) # rendering the image
                        
    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            
            # loop all valid moves
            for move in piece.moves:
                #color
                color = theme.moves.light if ((move.final.row + move.final.col) & 1 == 0) else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                #blit it
                pygame.draw.rect(surface, color, rect)
                
    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)
                
    def show_check(self, surface):
        theme = self.config.theme
        if Piece.KingInCheck:
            #color
            color = CHECKMATE if Board.checkmate else CHECK
            # rect
            if(self.constants.next_player == "white"):
                row, col = Piece.KingSquares[0]
            else:
                row, col = Piece.KingSquares[1]
            rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
            #blit it
            pygame.draw.rect(surface, color, rect)
                
    def show_hover(self, surface ):
        if self.hovered_sqr:
                # color
                color = HOVERED_COLOR
                # rect
                rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect, width=3)
                
    def display_message(self, screen, message):
        font = pygame.font.SysFont('Arial', 80, bold=True)
        msg = font.render(message, True, (255, 255, 255))  # White text

        right_x_position = WIDTH + WIDTH_OFFSET - 200

        padding = 20
        msg_rect = msg.get_rect()
        background_rect = pygame.Rect(
            right_x_position - msg_rect.width - 2 * padding,
            HEIGHT - msg_rect.height - 2 * padding,
            msg_rect.width + 2 * padding,
            msg_rect.height + 2 * padding
        )

        # Draw background (e.g., dark blue) with border radius for rounded edges
        pygame.draw.rect(screen, (0, 0, 128), background_rect, border_radius=10)

        pygame.draw.rect(screen, (255, 215, 0), background_rect, 5, border_radius=10)

        shadow_offset = 5
        shadow_msg = font.render(message, True, (0, 0, 0))  # Shadow text in black
        shadow_msg_rect = shadow_msg.get_rect(bottomright=(right_x_position - padding + shadow_offset, HEIGHT - padding + shadow_offset))
        screen.blit(shadow_msg, shadow_msg_rect)

        # Draw the message itself in white
        msg_rect = msg.get_rect(bottomright=(right_x_position - padding, HEIGHT - padding))
        screen.blit(msg, msg_rect)
            
    def render_right_side(self):
        return self.right_side.render(player1=self.white, player2=self.black, winner=self.winner, material=self.board.material, move_list=self.constants.move_list, scroll_y=self.scroll_y) # returns the play button
    # other methods
    
    def toggle_engine_mode(self):
        self.engine_mode = not self.engine_mode
         
        # stop current black players timer
        if self.current_player != self.white:
            self.black.stop_timer()
        
        if self.engine_mode:
            self.engine.time = self.player2.time
            self.black = self.engine
        else:
            self.player2.time = self.engine.time
            self.black = self.player2
        
        # update current Player
        self.current_player = self.white if self.current_player == self.white else self.black
        
        if self.current_player != self.white:
            self.black.start_timer()
        
    def start_game(self):
        if not self.start:
            self.start = True
            self.current_player.start_timer()
        sound = Sound(os.path.join('assets/sounds/move.wav'))
        sound.play()
    
    def next_turn(self):       
        
        self.current_player.stop_timer()
        # switch players
        self.current_player = self.black if self.current_player == self.white else self.white
        
        self.current_player.start_timer()
        
        self.constants.next_player = "white" if self.constants.next_player == "black" else "black"
        self.constants.ply += 1
        
        current_fen = self.board.getFEN()
        self.constants.history.append(current_fen)
        
    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hovered_sqr = self.board.squares[row][col]    
        
    def change_theme(self):
        self.config.change_theme()
        
    def play_sound(self, captured=False):
        if(captured):
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
            
    def reset(self):
        self.__init__(surface=self.surface)
        Board.checkmate = False
        Board.stalemate = False
        Piece.KingInCheck = False
        Piece.KingSquares = [(7, 4), (0, 4)] # white, black
    
    @staticmethod
    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"
