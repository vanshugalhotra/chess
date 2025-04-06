import pygame
from const import *
import os
import sys
import copy
import time

from utils import Sound
from gui import RightPanel,Themes, Dragger
from network import ChessClient
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
        
        self.flip_board = False
    
        initial_time = INITIAL_TIME
        
        self.white = Player("Vanshu Galhotra", "me.png", initial_time=initial_time)
        self.player2 = Player("Chamar", "chamar.png", initial_time=initial_time)
        self.black = self.player2
        self.engine = Player("Ustaad Ji", "ustaad.png", initial_time=initial_time)
        self.current_player = self.white
        
        self.winner = None
        
        self.scroll_y = 0
        
        self.last_move_info = None
        self.analysis = False
        
        self.right_side = RightPanel(surface=self.surface, player1=self.white, player2=self.black, winner=self.winner)
        
    # render methods        
    def update_screen(self, surface):
        self.show_chess_board(surface) 
        self.show_last_move(surface) 
        self.show_check(surface)
        self.show_moves(surface)  
        self.show_pieces(surface)
        self.show_hover(surface)
        if(self.analysis): 
            self.draw_analysis_popup(surface)

        if self.dragger.dragging:
            self.dragger.update_blit(surface)
    
    def show_chess_board(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                frow = 7 - row if self.flip_board else row
                fcol = 7 - col if self.flip_board else col 
                
                color = theme.bg.light if ((row + col) & 1 == 0) else theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                
                # row coordinates
                if col == 0:
                    color = theme.bg.dark if (row % 2 == 0) else theme.bg.light
                    
                    # label
                    lbl = self.config.font.render(str(ROWS-frow), 1, color)
                    lbl_pos = (5, 5+row*SQSIZE)
                    
                    #blit
                    surface.blit(lbl, lbl_pos)
                
                # col coordinates
                if row == 7:
                    color = theme.bg.dark if ( (row + col) % 2 == 0) else theme.bg.light 
                    
                    # label
                    lbl = self.config.font.render(Square.get_alphacode(fcol), 1, color)
                    lbl_pos = (col*SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    
                    #blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # Calculate the row and column based on flip_board
                render_row = 7 - row if self.flip_board else row
                render_col = 7 - col if self.flip_board else col

                # piece ?
                if self.board.squares[render_row][render_col].has_piece():  # if we have a piece on a particular square
                    piece = self.board.squares[render_row][render_col].piece
                    # all pieces except the dragging one
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)  # getting image path into image object
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2  # centering the image
                        piece.texture_rect = img.get_rect(center=img_center)  # coordinates
                        surface.blit(img, piece.texture_rect)  # rendering the image
                                
    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            
            # loop all valid moves
            for move in piece.moves:
                # Calculate the row and column based on flip_board
                final_row = 7 - move.final.row if self.flip_board else move.final.row
                final_col = 7 - move.final.col if self.flip_board else move.final.col

                # color
                color = theme.moves.light if ((final_row + final_col) & 1 == 0) else theme.moves.dark
                # rect
                rect = (final_col * SQSIZE, final_row * SQSIZE, SQSIZE, SQSIZE)
                # blit it
                pygame.draw.rect(surface, color, rect)
                    
    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial, final]:
                # Calculate the row and column based on flip_board
                render_row = 7 - pos.row if self.flip_board else pos.row
                render_col = 7 - pos.col if self.flip_board else pos.col

                # color
                color = theme.trace.light if (render_row + render_col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (render_col * SQSIZE, render_row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                
    def show_check(self, surface):
        if Piece.KingInCheck:
            # color
            color = CHECKMATE if Board.checkmate else CHECK
            # rect
            if self.constants.next_player == "white":
                row, col = Piece.KingSquares[0]
            else:
                row, col = Piece.KingSquares[1]
            
            # Calculate the row and column based on flip_board
            render_row = 7 - row if self.flip_board else row
            render_col = 7 - col if self.flip_board else col

            rect = (render_col * SQSIZE, render_row * SQSIZE, SQSIZE, SQSIZE)
            # blit it
            pygame.draw.rect(surface, color, rect)
                
    def show_hover(self, surface ):
        if self.hovered_sqr:
                # color
                color = HOVERED_COLOR
                # rect
                rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect, width=3)
                
    def show_popup(self, screen, text, animation_type="spinner", angle=0):
        """
        Display a pop-up with text and an optional animation (spinner or tick mark).

        Parameters:
            screen: The Pygame screen surface to draw on.
            text: The text to display in the pop-up.
            animation_type: The type of animation ("spinner" or "tick").
            angle: The current angle for the spinner animation (used for rotation).

        Returns:
            The updated angle for the spinner animation.
        """
        # Font and text settings
        font = pygame.font.SysFont('Arial', 32, bold=True)
        max_line_width = 350  # Maximum width for text before wrapping
        line_height = 40  # Height of each line of text

        # Wrap the text into multiple lines if it's too long
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            # Check if adding the next word exceeds the max line width
            test_line = current_line + " " + word if current_line else word
            test_width, _ = font.size(test_line)
            if test_width > max_line_width:
                lines.append(current_line)  # Add the current line to the list
                current_line = word  # Start a new line
            else:
                current_line = test_line  # Add the word to the current line
        if current_line:
            lines.append(current_line)  # Add the last line

        # Calculate popup dimensions based on the number of lines
        popup_width = max_line_width + 50  # Add padding
        popup_height = len(lines) * line_height + 120  # Add padding for animation and margins
        popup_x, popup_y = (WIDTH - popup_width) // 2, (HEIGHT - popup_height) // 2

        # Colors
        background_color = (40, 40, 40)  # Dark gray background
        border_color = (80, 80, 80)  # Soft border color
        text_color = (255, 255, 255)  # White text
        spinner_color = (100, 180, 255)  # Cool blue spinner
        tick_color = (0, 255, 0)  # Green tick mark

        # Create popup surface with transparency
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((0, 0, 0, 0))  # Transparent background

        # Draw popup with rounded corners
        pygame.draw.rect(popup_surface, background_color, (0, 0, popup_width, popup_height), border_radius=20)
        pygame.draw.rect(popup_surface, border_color, (0, 0, popup_width, popup_height), width=3, border_radius=20)

        # Render and blit each line of text
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect(center=(popup_width // 2, 40 + i * line_height))
            popup_surface.blit(text_surface, text_rect)

        # Draw the animation (spinner or tick mark)
        if animation_type == "spinner":
            # Draw a spinner (rotating arc)
            spinner_radius = 30
            spinner_center = (popup_width // 2, popup_height - 55)

            num_segments = 12  # Number of small segments forming the ring
            segment_angle = 2 * 3.1416 / num_segments  # Angle per segment

            for i in range(num_segments):
                segment_color = spinner_color if i % 3 == 0 else (spinner_color[0], spinner_color[1], spinner_color[2], 100)  # Alternate opacity
                start_angle = angle + i * segment_angle  # Rotate each segment
                end_angle = start_angle + segment_angle / 2  # Thin segment
                
                pygame.draw.arc(
                    popup_surface,
                    segment_color,
                    (spinner_center[0] - spinner_radius, spinner_center[1] - spinner_radius, spinner_radius * 2, spinner_radius * 2),
                    start_angle, end_angle, 5  # Line thickness
                )

            # Update angle for the next frame
            angle = (angle + 0.3) % (2 * 3.1416)  # Keep rotating smoothly

        elif animation_type == "tick":
            # Draw a tick mark (checkmark)
            tick_radius = 30
            tick_center = (popup_width // 2, popup_height - 55)

            # Draw the tick mark using lines
            pygame.draw.line(
                popup_surface,
                tick_color,
                (tick_center[0] - tick_radius // 2, tick_center[1]),
                (tick_center[0], tick_center[1] + tick_radius // 2),
                width=5
            )
            pygame.draw.line(
                popup_surface,
                tick_color,
                (tick_center[0], tick_center[1] + tick_radius // 2),
                (tick_center[0] + tick_radius // 2, tick_center[1] - tick_radius // 2),
                width=5
            )

        # Blit the popup surface onto the main screen
        screen.blit(popup_surface, (popup_x, popup_y))

        # Update the display
        pygame.display.update()

        # Return the updated angle for the spinner animation
        return angle

    def draw_analysis_popup(self, surface):
        info = self.last_move_info
        if not info:
            return

        elapsed = pygame.time.get_ticks() - info["time"]
        if elapsed > 3000:
            self.last_move_info = None
            return

        row, col = info["square"]
        if self.flip_board:
            row, col = 7 - row, 7 - col

        square_x = col * SQSIZE
        square_y = row * SQSIZE

        popup_width = 150
        popup_height = 40
        popup_x = square_x + SQSIZE // 2 - popup_width // 2
        if square_y - popup_height - 5 < 0:
            popup_y = square_y + SQSIZE + 5  # too high, draw below
        else:
            popup_y = square_y - popup_height - 5

        # Background
        pygame.draw.rect(surface, (255, 255, 240), (popup_x, popup_y, popup_width, popup_height), border_radius=10)
        pygame.draw.rect(surface, (180, 180, 180), (popup_x, popup_y, popup_width, popup_height), 2, border_radius=10)

        # Fonts
        font = pygame.font.SysFont("Arial", 18, bold=True)
        icon_surf = font.render(info["icon"], True, info["color"])
        label_surf = font.render(info["classification"], True, (0, 0, 0))

        # Icon (colored dot)
        surface.blit(icon_surf, (popup_x + 10, popup_y + popup_height // 2 - icon_surf.get_height() // 2))

        # Label text
        surface.blit(label_surf, (popup_x + 40, popup_y + popup_height // 2 - label_surf.get_height() // 2))

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
        Piece.KingSquares = [(7, 4), (0, 4)]
        self.constants.prev_score = 0
        
        return self

    def make_move(self, algebraic_move: str):
        initial_row, initial_col = Square.parseSquare(algebraic_move[0:2])
        final_row, final_col = Square.parseSquare(algebraic_move[2:])
        
        # create new move
        initial = Square(initial_row, initial_col)
        final_piece = self.board.squares[final_row][final_col].piece
        final = Square(final_row, final_col, final_piece)
        
        move = Move(initial, final)
        piece = copy.deepcopy(self.board.squares[initial_row][initial_col].piece)
        
        self.board.calc_moves(piece, initial_row, initial_col)
        self.board.make_move(piece, move)
        
    def toggle_analysis(self):
        self.constants.prev_score = 0
        if(self.analysis):
            self.analysis = False
            return "ON"
        self.analysis = True
        return "OFF"

