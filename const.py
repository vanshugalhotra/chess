# screen dimensions
WIDTH = 700
HEIGHT = 700

WIDTH_OFFSET = 740
HEIGHT_OFFSET = 0

# Board dimensions
ROWS = 8
COLS = 8

SQSIZE = WIDTH // COLS

# color
HOVERED_COLOR = (60, 50, 150)
CHECKMATE = '#ff4500'
CHECK = '#dc143c'
MESSAGE = '#dc143c'
BACKGROUND = '#312e2b'

class Constants:
    def __init__(self):
        self.next_player = "white"
        self.ply = 1 # no of half moves
        self.fiftyMove = 0
        self.enPas = None # enPas square


# ! need to refactor - in check

# todo: Check Effect  ✅
# todo: Checkmate ✅
# todo: Stalemate
# todo: Clock and move list
# todo: FEN Parser
# todo: UCI Protocol
# todo : MENU BAR
# todo: promotion bug fix
# todo: fiftyMove and 3 rep
