
class Move:
    
    def __init__(self, initial, final):
        # these are squares
        self.initial = initial
        self.final = final
        
    def __str__(self):
        ranki = 8 - (self.initial.row)
        filei = chr(ord('a') + self.initial.col)
        rankf = 8 - (self.final.row)
        filef = chr(ord('a') + self.final.col)
        s = f'{filei}{ranki}{filef}{rankf}'
        return s
        
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    
    
    @staticmethod
    def algebraic_notation(piece, move, isCapture=False, isCheck=False, isCheckMate=False, isPromotion=False, isEnPas=False, castle=""):
        notation = ""
        if castle:
            notation = "O-O" if castle.lower() == 'k' else 'O-O-O'
            return notation
        
        if not piece.name == "pawn":
            notation += piece.notation.upper()
            
        if isCapture:
            if piece.name == "pawn":
                notation += move.initial.get_notation()[0]
            notation += 'x'
        notation += move.final.get_notation()
        
        if isPromotion:
            notation += '=Q'

        if isCheckMate:
            notation += '#'
        elif isCheck:
            notation += '+'
        
        return notation