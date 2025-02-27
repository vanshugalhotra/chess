import pygame
from const import *
import time
import os


from utils import Sound, Position
from gui import RightPanel,Themes, Dragger
from game import Board, Piece, Move, Player, Square

class GameWindow:
    def __init__(self, surface):
        self.hovered_sqr = None
        self.constants = Constants()
        self.board = Board(self.constants)
        self.dragger = Dragger()
        self.config = Themes()
        
        self.surface = surface
        
        self.start = False
        self.engine_mode = False
        
    
        initial_time = INITIAL_TIME
        
        self.white = Player("Vanshu Galhotra", "me.png", initial_time=initial_time)
        self.player2 = Player("Inderpreet", "prem.png", initial_time=initial_time)
        self.black = self.player2
        self.engine = Player("Ustaad Ji", "ustaad.png", initial_time=initial_time)
        self.current_player = self.white
        
        self.winner = None
        
        self.scroll_y = 0
        
        self.right_side = RightPanel(surface=self.surface, player1=self.white, player2=self.black, winner=self.winner)
        
    # render methods
    def show_chess_board(self, surface):
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
        msg = font.render(message, True, WHITE)  # White text

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

