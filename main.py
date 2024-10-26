import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move
from board import Board
from engine import constants, uci, init, pvtable
import copy
import time
from piece import *
import threading

import traceback

log_file = open('error.log', 'w')
# original_stdout = sys.stdout
original_stderr = sys.stderr

# sys.stdout = log_file
sys.stderr = log_file

class Main: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH+WIDTH_OFFSET, HEIGHT+HEIGHT_OFFSET), pygame.DOUBLEBUF)
        pygame.display.set_caption("ਉਸਤਾਦ ਜੀ")
        self.game = Game(surface=self.screen)
        self.screen.fill(BACKGROUND)  

        self.engine_board = constants.Board()
        self.engine_info = constants.SEARCHINFO()

        self.engine_running = False
        self.bestMove = None
        init.AllInit()
        pvtable.InitPvTable(self.engine_board.PvTable)
    
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        clock = pygame.time.Clock()
        
        while True:
            
            try:
                self.screen.fill(BACKGROUND)  
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_check(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)
                
                play_button = game.render_right_side()
                
                if dragger.dragging:
                    dragger.update_blit(screen)
                    
                if Board.checkmate:
                    self.game.winner = self.game.current_player
                    game.display_message(screen, "Checkmate!!")
                    game.current_player.stop_timer()
                    
                if Board.stalemate:
                    game.display_message(screen, "Stalemate!!")
                    game.current_player.stop_timer()
                    
                if Board.repetition:
                    game.display_message(screen, "Draw (By Repetition)")
                    game.current_player.stop_timer()
                    
                if self.game.current_player.time <= 0:
                    self.game.winner = self.game.black if self.game.current_player == self.game.black else self.game.white
                    game.display_message(screen, "Timeout!!")
                                                        
                # event handling
                for event in pygame.event.get():
                    if not Board.checkmate and not Board.repetition:
                        # click event
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            
                            # checking for scroll events
                            if event.button == 4:
                                self.game.scroll_y -= 10
                            elif event.button == 5: # scroll down
                                self.game.scroll_y += 10
                                
                            # self.game.scroll_y = max(0, min(self.game.scroll_y, self.game.max_scroll))
                            
                            # checking for play button click
                            if event.button == 1:  # Left mouse button
                                mouse_pos = pygame.mouse.get_pos()
                                # Check if the button was clicked
                                if play_button.collidepoint(mouse_pos):
                                    game.start_game() # Set start to True when clicked
                                                            
                            if not game.start: # till game is started
                                continue
                            
                            dragger.update_mouse(event.pos) # event.pos will give (x, y) where the click event was made
                            
                            clicked_row = dragger.mouseY // SQSIZE # getting the row which we clicked
                            clicked_col = dragger.mouseX // SQSIZE
                            
                            # if theres a piece on the clicked area
                            if board.squares[clicked_row][clicked_col].has_piece():
                                piece = board.squares[clicked_row][clicked_col].piece
                                
                                # valid piece color?
                                if piece.color == game.constants.next_player:
                                    board.calc_moves(piece, clicked_row, clicked_col, wannaCheck=True)
                                    dragger.save_initial(event.pos)
                                    dragger.drag_piece(piece)
                                    
                                    #show methods
                                    game.show_bg(screen)
                                    game.show_check(screen)
                                    game.show_last_move(screen)
                                    game.show_moves(screen)
                                    game.show_pieces(screen)
                        
                        # mouse motion
                        elif event.type == pygame.MOUSEMOTION:
                            motion_row = event.pos[1] // SQSIZE
                            motion_col = event.pos[0] // SQSIZE
                            game.set_hover(motion_row, motion_col)
                            
                            if dragger.dragging: # mouse motion is active everytime we move mouse, we need to drag a piece only if dragging is True
                                dragger.update_mouse(event.pos) # first update the mouse position,
                                
                                game.show_bg(screen)
                                game.show_check(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                game.show_hover(screen)
                                dragger.update_blit(screen)
                                
                        
                        # click release
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if dragger.dragging:
                                dragger.update_mouse(event.pos)
                                
                                released_row = dragger.mouseY // SQSIZE
                                released_col = dragger.mouseX // SQSIZE
                                
                                # create possible move
                                initial = Square(dragger.initial_row, dragger.initial_col)
                                final = Square(released_row, released_col)
                                
                                move = Move(initial, final)
                                
                                # valid move
                                if board.valid_move(dragger.piece, move):
                                    captured = board.squares[released_row][released_col].has_piece()
                                    
                                    board.move(dragger.piece, move)
                                    
                                    # play sound
                                    game.play_sound(captured)
                                    # draw or show methods
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_check(screen)
                                    game.show_pieces(screen)
                                                                        
                                    # change the turn
                                    game.next_turn()
                                    
                                
                                else: # if just picked it and not moved
                                    dragger.piece.clear_moves()
                            
                            dragger.undrag_piece()
                        
                        
                    # key press events
                    if event.type == pygame.KEYDOWN:
                        # key pressed "t"
                        if event.key == pygame.K_t:
                            game.change_theme()
                            
                        # key pressed "r"
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            
                        # key pressed "m"
                        if event.key == pygame.K_m:
                            game.toggle_engine_mode()
                            game.display_message(screen, "Changed Mode!!!")
                            continue
                        
                        # key pressed "p"
                        if event.key == pygame.K_p:
                            game.display_message(screen, "Play!!")
                            self.game.start_game()
                    
                    # quit
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                if(game.current_player == game.black and self.game.engine_mode):
                    # draw or show methods
                    game.show_bg(screen)
                    game.show_last_move(screen)
                    game.show_check(screen)
                    game.show_pieces(screen) 
                    pygame.display.update()
                    clock.tick(60)
                    
                    self.move_engine()
                    
                pygame.display.update()
                clock.tick(60)
            
            except Exception as e:
                traceback.print_exc(file=sys.stderr)
                print(e.args)
                print("Check Error LOG")
    
    def move_engine(self):
        if(self.bestMove):
            initial_row, initial_col = Square.parseSquare(self.bestMove[0:2])
            final_row, final_col = Square.parseSquare(self.bestMove[2:])
            
            # create new move
            initial = Square(initial_row, initial_col)
            final_piece = self.game.board.squares[final_row][final_col].piece
            final = Square(final_row, final_col, final_piece)
            
            
            move = Move(initial, final)
            piece = copy.deepcopy(self.game.board.squares[initial_row][initial_col].piece)
            
            self.game.board.calc_moves(piece, initial_row, initial_col)
            self.game.board.move(piece, move)
            self.bestMove = None # resetting the bestMove
            self.game.next_turn()
            self.engine_running = False
            return 

        if self.engine_running:
            return
        
        currentFen = self.game.board.getFEN()
        command = f'position fen {currentFen}'
        
        uci.ParsePosition(command, self.engine_board)
        
        # command = f'go wtime 320000 btime 300000 winc 20000 binc 20000'
        depth = 6
        if self.game.constants.ply < 10:
            depth = 5
        elif self.game.constants.ply >= 10 and self.game.constants.ply <= 60:
            depth = 6
        else:
            depth = 8
            
        wtime = self.game.white.time * 1000
        btime = self.game.black.time * 1000
        movestogo = 30
        
        command = f'go depth {depth} wtime {wtime} btime {btime} movestogo {movestogo}'
        print(command)
        
        def calculate_best_move():
            self.bestMove = uci.ParseGo(command, self.engine_info, self.engine_board)
        
        bestmove_thread = threading.Thread(target=calculate_best_move)
        self.engine_running = True
        bestmove_thread.start()
            
main = Main()
main.mainloop()

sys.stderr = original_stderr
log_file.close()