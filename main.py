import pygame
import sys
from const import *
from gui import GameWindow
from game import Board, EventHandler, ChessEngine
import traceback

log_file = open('error.log', 'w')
original_stderr = sys.stderr

sys.stderr = log_file

class Main: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH+WIDTH_OFFSET, HEIGHT+HEIGHT_OFFSET), pygame.DOUBLEBUF)
        pygame.display.set_caption(f"{NAME} {VERSION} - by {AUTHOR}\t\tEngine {VERSION} ( {ENGINE} ) - by {AUTHOR}")
        
        self.game = GameWindow(surface=self.screen)
        self.screen.fill(BACKGROUND)  
        
        self.event_handler = EventHandler(game=self.game, screen=self.screen)
        
        # engine things
        self.engine = ChessEngine(game=self.game)
        
        self.userMove = None
    
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        dragger = self.game.dragger

        clock = pygame.time.Clock()
        
        while True:
            
            try:
                self.screen.fill(BACKGROUND)  
                
                game.update_screen(screen)
                
                play_button = game.render_right_side()
                self.event_handler.set_play_button(play_button=play_button)
                
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
                
                self.event_handler.handle_events()
                
                if(game.current_player == game.black and self.game.engine_mode):
                    # draw or show methods
                    game.update_screen(screen)
                    pygame.display.update()
                    clock.tick(60)
                    
                    self.engine.make_best_move()
                    
                pygame.display.update()
                clock.tick(60)
            
            except Exception as e:
                traceback.print_exc(file=sys.stderr)
                print(e.args)
                print("Check Error LOG")
        
main = Main()
main.mainloop()

sys.stderr = original_stderr
log_file.close()