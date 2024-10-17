from const import *
from square import Square
from piece import *
from move import Move

class Board:
    
    def __init__(self):
        self.squares = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        self._create()
        
        self._add_pieces('white')
        self._add_pieces('black')
        
        self.last_move = None
    
    def calc_moves(self, piece, row, col):
        """
        Calculate all the possible (valid) moves of an specific piece on a specific position
        
        """
        
        def pawn_moves():
            steps = 1 if piece.moved else 2
            
            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # create a new move
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: # means we are blocked
                        break
                else: # not in range
                    break
                
            # diagonal moves
            move_row = row + piece.dir
            move_cols = [col - 1, col + 1] # to left and to right
            
            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        # create a new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        
                        move = Move(initial, final)
                        piece.add_move(move)
        
        
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col-1),
                (row-2, col+1),
                (row+2, col-1),
                (row+2, col+1),
                (row-1, col-2),
                (row-1, col+2),
                (row+1, col-2),
                (row+1, col+2),
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        
                        # create new move
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        move = Move(initial, final)
                        piece.add_move(move)
        
        def straighline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        
                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)
                        
                        # has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break
                        
                        # has team piece
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                                        
                    else:
                        break
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr
            
        def king_moves():
            adjs = [
                (row-1, col+1), # up-right
                (row+1, col+1), # down-right
                (row+1, col-1), # down-left
                (row-1,col-1), # up-left
                (row-1,col+0), # up
                (row+0, col-1), # left
                (row+1, col+0), # down
                (row+0, col+1) # right
            ]
            
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        move = Move(initial, final)
                        
                        piece.add_move(move)
                        
            # castling moves
            if not piece.moved:
                #queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): # castling is not possible because there are pieces between
                                break
                            
                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook
                                
                                # rook Move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                move = Move(initial, final)
                                left_rook.add_move(move)
                                
                                
                                # king move
                                
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)
                                
                #king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): # castling is not possible because there are pieces between
                                break
                            
                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook
                                
                                # rook Move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move = Move(initial, final)
                                right_rook.add_move(move)
                                
                                
                                # king move
                                
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)
                                

        
        if isinstance(piece, Pawn): # if piece is the instance of Pawn class
            pawn_moves()
        
        elif isinstance(piece, Knight):
            knight_moves()
        
        elif isinstance(piece, Bishop):
            straighline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1) # down-left
            ])
        
        elif isinstance(piece, Rook):
            straighline_moves([
                (-1, 0), # up
                (0, 1), # left
                (1, 0), # down
                (0, -1) # right
            ])
        
        elif isinstance(piece, Queen):
            straighline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
                (-1, 0), # up
                (0, 1), # left
                (1, 0), # down
                (0, -1) # right
            ])
        
        elif isinstance(piece, King):
            king_moves()
    
    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def move(self, piece, move):
        initial = move.initial
        final = move.final
        
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)
        
        piece.moved = True
        
        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])
        
        # clear valid moves
        piece.clear_moves()
        
        self.last_move = move
    
    
    # starting with _ represents them as private methods
    def _create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)
        
        # pawn
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            
        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
            
        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
            
        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
            
        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
    