import pygame
from const import *
from board import Board
from config import Config
from square import Square
from dragger import Dragger
from piece import Piece
from player import Player

class Game:
    
    def __init__(self):
        self.hovered_sqr = None
        self.constants = Constants()
        self.board = Board(self.constants)
        self.dragger = Dragger()
        self.config = Config()
        self.player1 = Player("Vanshu", "me.png")
        self.player2 = Player("UstaadJI", "ustaad.png")
        
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
    
    def show_players(self, surface):
        # Adjusted card dimensions and spacing
        padding_left = 20
        card_width = 180  # Reduced card width
        card_height = 220  # Reduced card height
        image_size = 170  # Adjust image size to fit the card width
        padding = (WIDTH_OFFSET - 2 * (card_width + padding_left))  # Adjust space between the two cards

        # Card positions for player1 (left) and player2 (right)
        pos_x1 = WIDTH + padding_left  # X position for player1
        pos_y1 = 10   # Y position for both players
        pos_x2 = pos_x1 + card_width + padding  # X position for player2

        # Background color for card (darker than the screen background)
        card_color = (41, 40, 38)  # A darker grey (close to #312e2b, slightly darker)

        # Shadow color for floating effect (reduced further)
        shadow_color = (0, 0, 0, 30)  # Lighter black for subtle shadow

        # Text properties
        font = pygame.font.SysFont('Arial', 22, bold=True)  # Slightly smaller font for name
        text_color = (255, 255, 255)  # White text

        # Function to draw each player's card
        def draw_player_card(player, pos_x, pos_y):
            # Load and scale player image (HD image with ideal resolution)
            player_img = pygame.image.load(player.image)
            player_img = pygame.transform.scale(player_img, (image_size, image_size))

            # Create the shadow effect (minimal offset)
            shadow_rect = pygame.Rect(pos_x + 1, pos_y + 1, card_width, card_height)
            pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=15)

            # Create the card background
            card_rect = pygame.Rect(pos_x, pos_y, card_width, card_height)
            pygame.draw.rect(surface, card_color, card_rect, border_radius=15)

            # Blit the player image (covering the entire top part of the card)
            surface.blit(player_img, (pos_x, pos_y))

            # Render the player's name and slightly stretch horizontally
            player_name = font.render(player.name, True, text_color)
            # Slight horizontal stretch for the name text
            player_name_stretched = pygame.transform.scale(player_name, (player_name.get_width() + 20, player_name.get_height()))
            name_rect = player_name_stretched.get_rect(center=(pos_x + card_width // 2, pos_y + image_size + 30))  # Adjusted name placement
            surface.blit(player_name_stretched, name_rect)

        # Draw the cards for both players
        draw_player_card(self.player1, pos_x1, pos_y1)  # Player 1 on the left
        draw_player_card(self.player2, pos_x2, pos_y1)  # Player 2 on the right







        
    # other methods
    
    def next_turn(self):
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