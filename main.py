import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move

class Main: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ਉਸਤਾਦ ਜੀ")
        self.game = Game()
    
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        
        while True:
            
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                
                # click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos) # event.pos will give (x, y) where the click event was made
                    
                    clicked_row = dragger.mouseY // SQSIZE # getting the row which we clicked
                    clicked_col = dragger.mouseX // SQSIZE
                    
                    # if theres a piece on the clicked area
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        
                        # valid piece color?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)
                    
                    if dragger.dragging: # mouse motion is active everytime we move mouse, we need to drag a piece only if dragging is True
                        dragger.update_mouse(event.pos) # first update the mouse position,
                        
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                        
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        
                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        # valid move
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            
                            board.move(dragger.piece, move)
                            
                            board.set_true_en_passsant(dragger.piece)
                            # play sound
                            game.play_sound(captured)
                            
                            # draw or show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            
                            # change the turn
                            game.next_turn()
                        
                        else: # if just picked it and not moved
                            dragger.piece.clear_moves()
                    
                    dragger.undrag_piece()
                
                # key press events
                elif event.type == pygame.KEYDOWN:
                    # key pressed "t"
                    if event.key == pygame.K_t:
                        game.change_theme()
                        
                    # key pressed "r"
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                
                # quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            
            pygame.display.update()

main = Main()
main.mainloop()