

class Move:
    
    def __init__(self, initial, final):
        # these are squares
        self.initial = initial
        self.final = final
        
    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {initial.row})'
        s += f' -> ({self.final.col}, {final.row})'
        return s
    
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final