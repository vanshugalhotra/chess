# screen dimensions
WIDTH = 650
HEIGHT = 650

# Board dimensions
ROWS = 8
COLS = 8

SQSIZE = WIDTH // COLS

# color
HOVERED_COLOR = (60, 50, 150)
CHECKMATE = '#ff4500'
CHECK = '#dc143c'
MESSAGE = '#dc143c'

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
# todo: FEN Parser
# todo: UCI Protocol
