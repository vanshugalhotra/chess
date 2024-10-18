from const import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os

class Board:
    
    def __init__(self):
        self.squares = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        self._create()
        
        self._add_pieces('black')
        self._add_pieces('white')
        self.last_move = None
        
        
    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final
            
        en_passant_empty = self.squares[final.row][final.col].isempty()
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
                
        if isinstance(piece, Pawn):
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                
                if not testing:
                    sound = Sound(os.path.join('assets/sounds/capture.wav'))
                    sound.play()
                
            else:
                self.check_promotion(piece, final)
            
        # castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if diff < 0 else piece.right_rook
                self.move(rook, rook.moves[-1]) # need to move the rook 

        
        piece.moved = True
        
        # clear valid moves
        piece.clear_moves()
        self.last_move = move
    
        
    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
            
    def castling(self,initial, final):
        return abs(initial.col - final.col) == 2 # if the king moved by 2 squares
    
    def set_true_en_passsant(self, piece):
        if not isinstance(piece, Pawn):
            return 
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
                    
        piece.en_passant = True
            
    def in_check(self,piece, move): # checks if after moving the piece my king is in check or not
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self) # cloning our board
        
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves: #valid piece for the enemy's piece
                        if isinstance(m.final.piece, King):
                            return True
        return False
        
    
    def calc_moves(self, piece, row, col, bool=True):
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
                        
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
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
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)
                        move = Move(initial, final)
                        
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                                
        
            # en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            
            # left en_passant
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_rival_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final_piece = self.squares[row][col-1].piece
                            final = Square(fr, col-1, final_piece)
                            
                            move = Move(initial, final)
                            
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                                
            # right en_passant
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_rival_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final_piece = self.squares[row][col+1].piece
                            final = Square(fr, col+1, final_piece)
                            
                            move = Move(initial, final)
                            
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                                
        
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        
                        # create new move
                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        
                        move = Move(initial, final)
                        
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else: break
                        else:
                            piece.add_move(move)
                                
        
        def straighline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        
                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                                
                        
                        # has enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        
                        # has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                                        
                    else:
                        break
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr
            
        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        
                        move = Move(initial, final)
                        
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else: continue
                        else:
                            piece.add_move(move)
                
            # castling moves, make sure (we can't castle if we are in check, castle through check and into check)
            if not piece.moved:
                # queen side castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): # castling not possible
                                break
                            
                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook
                                
                                # rook Move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final) # can't castle into the check
                                
                                # king Move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final) # can't castle if check
                                
                                # if D1 is attacked then we can't castle queen side (for white) d8 for black
                                initial = Square(row, col)
                                final = Square(row, 3)
                                moveD = Move(initial, final) # cant castle through the check
                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR) and not self.in_check(piece, moveD):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)
                                    
                # king side castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): # castling not possible
                                break
                            
                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook
                                
                                # rook Move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final) # cant castle into the check
                                
                                # king Move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final) # cant castle if check
                                
                                # if F1 is attacked then we can't castle king side (for white) f8 for black
                                initial = Square(row, col)
                                final = Square(row, 5)
                                moveF = Move(initial, final) # cant castle through the check
                                
                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR) and not self.in_check(piece, moveF):
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)
                                    
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
    