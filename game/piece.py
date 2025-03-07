import os

class Piece:
    KingInCheck = False
    KingSquares = [(7, 4), (0, 4)] # white, black
    def __init__(self, name, color, value, notation="", texture=None, texture_rect=None):
        self.name = name
        self.color = color
        self.texture = texture # image path
        self.moves = []
        self.moved = False
        self.notation = notation
        
        value_sign = 1 if color == "white" else -1
        # self.value = value * value_sign
        self.value = value
        
        self.texture_rect = texture_rect
        
        self.set_texture()
        
    def set_texture(self, size=80): # image
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')
        
    def add_move(self, move):
        self.moves.append(move)
        
    def clear_moves(self):
        self.moves = []
        
    def get_notation(self):
        return self.notation if self.color == "black" else self.notation.upper()
        
class Pawn(Piece):
    
    def __init__(self, color):
        self.dir = -1 if color == "white" else 1
        super().__init__("pawn", color, 1, notation='p')
    
class Knight(Piece):
    
    def __init__(self, color):
        
        super().__init__("knight", color, 3, notation='n')

class Bishop(Piece):
    
    def __init__(self, color):
        
        super().__init__("bishop", color, 3, notation='b')

class Rook(Piece):
    
    def __init__(self, color):
        
        super().__init__("rook", color, 5, notation='r')

class Queen(Piece):
    
    def __init__(self, color):
        
        super().__init__("queen", color, 9, notation='q')
        
class King(Piece):
    
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__("king", color, 90000, notation='k')

