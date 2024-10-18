

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