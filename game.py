import pygame
from const import *
from board import Board
from dragger import Dragger
class Game:
    
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
    
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if( (row + col) & 1 == 0 ): # if is even
                    color = LIGHT_GREEN
                else:
                    color = DARK_GREEN
                    
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
            
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
        if self.dragger.dragging:
            piece = self.dragger.piece
            
            # loop all valid moves
            for move in piece.moves:
                #color
                color = '#C86464' if ((move.final.row + move.final.col) & 1 == 0) else '#C84646'
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                #blit it
                pygame.draw.rect(surface, color, rect)