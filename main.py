import pygame
import sys
from const import *
from game import Game

class Main: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game= Game()
    
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        
        while True:
            
            game.show_bg(screen)
            game.show_pieces(screen)
            
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
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging: # mouse motion is active everytime we move mouse, we need to drag a piece only if dragging is True
                        dragger.update_mouse(event.pos) # first update the mouse position,
                        
                        game.show_bg(screen)
                        game.show_pieces(screen)
                        
                        dragger.update_blit(screen)
                        
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()
                
                
                # quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            
            pygame.display.update()

main = Main()
main.mainloop()