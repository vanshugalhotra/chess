NAME = "Chess"
VERSION = "1.0.0"
AUTHOR = "Vanshu Galhotra"

ENGINE = "ਉਸਤਾਦ ਜੀ"


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

WHITE = "#ffffff"
RED = "FF0000"
BROWN = "#322D2A"
JET_BLACK = "#1E1E1E"
AMBER = "#f39c12"
MIDNIGHT_BLUE = "#2C3E50"
SKY_BLUE = "#3498DB"
YELLOW = "#F1C40F"
LIGHT_GRAY = "#F0F0F0"

class Constants:
    def __init__(self):
        self.next_player = "white"
        self.ply = 1 # no of half moves
        self.fiftyMove = 0
        self.enPas = None # enPas square
        self.history = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']
        self.move_list = [] 
        
# ! need to refactor - in check

# todo: Check Effect  ✅
# todo: Checkmate ✅
# todo: Clock ✅
# todo: winner banner ✅
# todo: FEN Parser
# todo: UCI Protocol
# todo : MENU BAR
# todo: flipping sides
# todo: take back moves
# todo: material count ✅
# todo: fiftyMove
# todo:  3 rep ✅

# todo: promotion bug fix ✅
# todo: bug fix in engine (makemove -> clearPiece) ✅
# todo: bug fix: clock time for engine ✅
# todo: bug fix: valid knight moves ✅
# todo: timeout bug fix
# todo: move list scrollbar bug 
# todo: Stalemate bug

"""
chess/
│
├── assets/                # No __init__.py needed (not a Python package)
│   └── pieces/            # No __init__.py needed
│
├── src/                   # No __init__.py needed (unless you want to import from src)
│   ├── game/              # Add __init__.py
│   │   ├── __init__.py    # Make game a package
│   │   ├── board.py
│   │   ├── move.py
│   │   ├── piece.py
│   │   ├── player.py
│   │   └── square.py
│   │
│   ├── gui/               # Add __init__.py
│   │   ├── __init__.py    # Make gui a package
│   │   ├── window.py
│   │   ├── components/    # Add __init__.py
│   │   │   ├── __init__.py  # Make components a package
│   │   │   ├── button.py
│   │   │   └── clock.py
│   │   ├── themes.py
│   │   └── dragger.py
│   │
│   ├── utils/             # Add __init__.py
│   │   ├── __init__.py    # Make utils a package
│   │   ├── color.py
│   │   ├── sound.py
│   │   └── const.py
│   │
│   └── main.py            # No __init__.py needed (not a package)
│
└── README.md

"""