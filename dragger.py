from const import *
import pygame

class Dragger:
    
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.piece = None
        self.dragging = False
    
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos # (x, y)
        
        
    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE
        
    def update_blit(self, surface):
        self.piece.set_texture(size=128) # when dragging we want that piece to be a little bit bigger than others
        
        img = pygame.image.load(self.piece.texture)
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)
    
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
        
    def undrag_piece(self):
        self.piece = None
        self.dragging = False
    