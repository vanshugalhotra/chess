
class Square:
    
    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    
    def __init__(self, row, col, piece=None):
        if Square.in_range(row, col):
            self.row = row
            self.col = col
            self.piece = piece
            self.alphacol = self.ALPHACOLS[col]
        
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __str__(self):
        file = chr(self.col + ord('a'))
        rank = 8 - self.row
        return f'{file}{rank}'
        
    def has_piece(self):
        return self.piece != None
    
    def isempty(self):
        return not self.has_piece()
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def isempty_or_rival(self, color):
        return self.isempty() or self.has_rival_piece(color)
    
    def get_notation(self):
        rank = 8 - (self.row)
        file = chr(ord('a') + self.col)
        
        return f'{file}{rank}'
        
    @staticmethod
    def in_range(*args): # not a class method, we can call static method with object
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
    @staticmethod
    def get_alphacode(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        
        return ALPHACOLS[col]
    
    @staticmethod 
    def parseSquare(square):
        file = square[0]
        rank = int(square[1])
        
        row = 8 - rank
        col = ord(file) - ord('a')
        return row,col
    