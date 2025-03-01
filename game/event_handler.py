import pygame
import sys
from const import SQSIZE
from game import Move, Square

class EventHandler:
    def __init__(self, game, screen):
        self.game = game
        self.board = self.game.board
        self.dragger = self.game.dragger
        self.screen = screen
        self.play_button = None

    def set_play_button(self, play_button):
        self.play_button = play_button
        
    def handle_events(self):
        for event in pygame.event.get():
            if not self.board.checkmate and not self.board.repetition:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_button_up(event)
                
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def handle_mouse_button_down(self, event):
        if event.button == 4:
            self.game.scroll_y -= 15
        elif event.button == 5:
            self.game.scroll_y += 15
        
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_button.collidepoint(mouse_pos):
                self.game.start_game()
        
        if not self.game.start:
            return
        
        self.dragger.update_mouse(event.pos)
        clicked_row, clicked_col = self.dragger.mouseY // SQSIZE, self.dragger.mouseX // SQSIZE
        
        if Square.in_range(clicked_row, clicked_col):
            if self.board.squares[clicked_row][clicked_col].has_piece():
                piece = self.board.squares[clicked_row][clicked_col].piece
                if piece.color == self.game.constants.next_player:
                    self.board.calc_moves(piece, clicked_row, clicked_col, wannaCheck=True)
                    self.dragger.save_initial(event.pos)
                    self.dragger.drag_piece(piece)
                    self.update_board()
    
    def handle_mouse_motion(self, event):
        motion_row, motion_col = event.pos[1] // SQSIZE, event.pos[0] // SQSIZE
        self.game.set_hover(motion_row, motion_col)
        
        if self.dragger.dragging:
            self.dragger.update_mouse(event.pos)
            self.update_board()
            self.game.show_hover(self.screen)
            self.dragger.update_blit(self.screen)
    
    def handle_mouse_button_up(self, event):
        if self.dragger.dragging:
            self.dragger.update_mouse(event.pos)
            released_row, released_col = self.dragger.mouseY // SQSIZE, self.dragger.mouseX // SQSIZE
            
            move = Move(Square(self.dragger.initial_row, self.dragger.initial_col),
                        Square(released_row, released_col))
            
            if move.is_valid(self.dragger.piece):
                captured = self.board.squares[released_row][released_col].has_piece()
                self.board.make_move(self.dragger.piece, move)
                self.game.play_sound(captured)
                self.update_board()
                self.game.next_turn()
            else:
                self.dragger.piece.clear_moves()
        
        self.dragger.undrag_piece()
    
    def handle_key_down(self, event):
        if event.key == pygame.K_t:
            self.game.change_theme()
        elif event.key == pygame.K_r:
            self.game.reset()
        elif event.key == pygame.K_m:
            self.game.toggle_engine_mode()
            self.game.display_message(self.screen, "Changed Mode!!!")
        elif event.key == pygame.K_p:
            self.game.display_message(self.screen, "Play!!")
            self.game.start_game()
    
    def update_board(self):
        self.game.update_screen(self.screen)