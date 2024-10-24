import pygame
from const import *
from board import Board
from config import Config
from square import Square
from dragger import Dragger
from piece import Piece
from player import Player
import time

class Game:
    
    def __init__(self):
        self.hovered_sqr = None
        self.constants = Constants()
        self.board = Board(self.constants)
        self.dragger = Dragger()
        self.config = Config()
        
        self.start = False
        self.engine_mode = False
        
        initial_time = 600
        
        self.white = Player("Vanshu Galhotra", "me.png", initial_time=initial_time)
        self.player2 = Player("Prem Pal", "prem.png", initial_time=initial_time)
        self.black = self.player2
        self.engine = Player("Ustaad Ji", "ustaad.png", initial_time=initial_time)
        self.current_player = self.white
        
        self.winner = None
        
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

            # msg background dimensions
            msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            background_rect = pygame.Rect(
                msg_rect.left - 20,  # Padding for background
                msg_rect.top - 20,
                msg_rect.width + 40,
                msg_rect.height + 40
            )

            # Draw background (e.g., dark blue)
            pygame.draw.rect(screen, (0, 0, 128), background_rect, border_radius=10)

            # Add a border around the background (e.g., gold color)
            pygame.draw.rect(screen, (255, 215, 0), background_rect, 5, border_radius=10)

            # Shadow effect (slightly offset black text)
            shadow_msg = font.render(message, True, (0, 0, 0))
            shadow_offset = 5
            screen.blit(shadow_msg, shadow_msg.get_rect(center=(WIDTH // 2 + shadow_offset, HEIGHT // 2 + shadow_offset)))

            # Draw the msg itself
            screen.blit(msg, msg_rect)
            
    def show_rightSide(self, surface):
        padding_left = 20
        card_width = 180 
        card_height = 220  
        image_size = 170  
        padding = (WIDTH_OFFSET - 2*(card_width + padding_left))  

        # Card positions for player1 (left) and player2 (right)
        pos_x1 = WIDTH + padding_left  # X position for player1
        pos_y1 = 20  
        pos_x2 = pos_x1 + card_width + padding  # X position for player2

        card_color = (50, 45, 42)  # Darker grey to contrast with the background

        shadow_offset = 8
        shadow_color = (30, 30, 30)  # Darker shadow color

        # Text properties
        font = pygame.font.SysFont('Arial', 22, bold=True)
        text_color = (255, 255, 255)  # White text
        
        # Start button properties
        button_width = 150
        button_height = 50
        button_color = (44, 62, 80)  # Dark Blue color (background)
        button_hover_color = (52, 152, 219)  # Brighter gradient-like blue on hover
        button_text_color = (241, 196, 15)  # Soft Yellow text
        shadow_color = (30, 30, 30)  # Dark shadow color
        shadow_offset = 5  # Distance for the shadow
        button_font = pygame.font.SysFont('Arial', 26, bold=True)

        # Calculate Start button position (centered between the two cards)
        button_x = (pos_x1 + card_width + pos_x2) // 2 - button_width // 2
        button_y = pos_y1 + card_height // 2 - button_height // 2 + 20

        def is_mouse_over_button(mouse_pos, rect):
            return rect.collidepoint(mouse_pos)

        def draw_start_button():
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            # Draw shadow
            shadow_rect = pygame.Rect(button_x + shadow_offset, button_y + shadow_offset, button_width, button_height)
            pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=10)
            
            if is_mouse_over_button(mouse_pos, button_rect):
                pygame.draw.rect(surface, button_hover_color, button_rect, border_radius=10)
            else:
                pygame.draw.rect(surface, button_color, button_rect, border_radius=10)

            button_text = button_font.render("PLAY", True, button_text_color)
            text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            surface.blit(button_text, text_rect)
            
            return button_rect

        # Function to draw each player's card
        def draw_player_card(player, pos_x, pos_y, clock_pos, clock_bg_color, clock_text_color, align):
            # Draw the shadow first, offset behind the card
            shadow_rect = pygame.Rect(pos_x + shadow_offset, pos_y + shadow_offset, card_width, card_height)
            pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=15)

            # Load and scale player image (HD image with ideal resolution)
            player_img = pygame.image.load(player.image)
            player_img = pygame.transform.scale(player_img, (image_size, image_size))

            # Create the card background
            card_rect = pygame.Rect(pos_x, pos_y, card_width, card_height)
            pygame.draw.rect(surface, card_color, card_rect, border_radius=15)

            # Blit the player image (covering the entire top part of the card)
            surface.blit(player_img, (pos_x, pos_y))

            # Render and display the player's name
            player_name = font.render(player.name, True, text_color)
            name_rect = player_name.get_rect(center=(pos_x + card_width // 2, pos_y + image_size + 30))
            surface.blit(player_name, name_rect)

            clock_width = 160  
            clock_height = 40  
            clock_rect = pygame.Rect(clock_pos[0], clock_pos[1], clock_width, clock_height)
            pygame.draw.rect(surface, clock_bg_color, clock_rect, border_radius=8) 

            # Render and display the player's time
            clock_font = pygame.font.SysFont('Lucida Console', 25, bold=True) 
            player_time = Game.format_time(player.time) 
            clock_surface = clock_font.render(player_time, True, clock_text_color)
            
            if align == 'right':
                clock_surface_rect = clock_surface.get_rect(right=clock_pos[0] + clock_width - 10, centery=clock_pos[1] + clock_height // 2)
            else:
                clock_surface_rect = clock_surface.get_rect(left=clock_pos[0] + 10, centery=clock_pos[1] + clock_height // 2)

            surface.blit(clock_surface, clock_surface_rect)

        def draw_winner_banner(player, pos_x, pos_y):
            banner_width = card_width
            banner_height = 40
            banner_color = '#f39c12'
            banner_text_color = '#ffffff'
            banner_font = pygame.font.SysFont('Arial', 24, bold=True)

            # Banner position (directly below the player's card)
            banner_x = pos_x
            banner_y = pos_y + card_height + 10  # Adjust the Y position slightly below the card

            # Draw the banner
            banner_rect = pygame.Rect(banner_x, banner_y, banner_width, banner_height)
            pygame.draw.rect(surface, banner_color, banner_rect, border_radius=8)

            # Render and display the banner text
            banner_text = banner_font.render("Winner!", True, banner_text_color)
            banner_text_rect = banner_text.get_rect(center=(banner_x + banner_width // 2, banner_y + banner_height // 2))
            surface.blit(banner_text, banner_text_rect)

        def draw_material_indicator(player_material, pos_x, pos_y):
            # Small circular indicator to show player advantage
            indicator_radius = 15
            indicator_bg_color = (240, 240, 240)  # Light shade of white
            indicator_text_color = (0, 0, 0)      # Black text
            circle_x = pos_x + card_width - indicator_radius + 10 # Bottom-right corner of the card
            circle_y = pos_y + card_height - indicator_radius + 20

            # Draw the circle indicator (background)
            pygame.draw.circle(surface, indicator_bg_color, (circle_x, circle_y), indicator_radius)

            # Render the player's material inside the indicator
            font = pygame.font.SysFont('Arial', 18, bold=True)
            material_txt = f'+{abs(self.board.material[0] - self.board.material[1])}'
            material_text = font.render(material_txt, True, indicator_text_color)
            text_rect = material_text.get_rect(center=(circle_x, circle_y))
            surface.blit(material_text, text_rect)


        clock_pos_player1 = (pos_x1 + card_width - 20, pos_y1 + 10) 
        draw_player_card(self.white, pos_x1, pos_y1, clock_pos_player1, (255, 255, 255), (255, 0, 0), align='right') 
        
        clock_pos_player2 = (pos_x2 - 150, pos_y1 + 10) 
        draw_player_card(self.black, pos_x2, pos_y1, clock_pos_player2, (30, 30, 30), (255, 255, 255), align='left') 
        
        button_rect = draw_start_button()
        
        if self.winner == self.white:
            draw_winner_banner(self.white, pos_x2, pos_y1)
        
        elif self.winner == self.black:
            draw_winner_banner(self.black, pos_x1, pos_y1)
            
        # Material advantage indicator logic
        if self.board.material[0] > self.board.material[1]:  # White has more material
            draw_material_indicator(self.board.material[0], pos_x1, pos_y1)
        elif self.board.material[1] > self.board.material[0]:  # Black has more material
            draw_material_indicator(self.board.material[1], pos_x2, pos_y1)
        
        return button_rect
        
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
        self.start = True
        self.current_player.start_timer()
    
    def next_turn(self):       
        # switch players
        
        self.current_player.stop_timer()
        
        self.current_player = self.black if self.current_player == self.white else self.white
        
        self.current_player.start_timer()
        
        self.constants.next_player = "white" if self.constants.next_player == "black" else "black"
        self.constants.ply += 1
        
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
        self.__init__()
        Board.checkmate = False
        Piece.KingInCheck = False
        Piece.KingSquares = [(7, 4), (0, 4)] # white, black
    
    
    @staticmethod
    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"
