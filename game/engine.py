from pychess_engine import Engine
import threading

class ChessEngine:
    def __init__(self, game, movestogo=40, elo=1500):
        self.engine = Engine(elo=elo)
        self.game = game
        self.bestMove = None
        self.movestogo = movestogo
        self.engine_running = False
        
    def make_best_move(self):
        if(self.bestMove):
            self.game.make_move(self.bestMove)
            self.bestMove = None # resetting the bestMove
            self.game.next_turn()
            self.engine_running = False
            return 

        if self.engine_running:
            return
        
        currentFen = self.game.board.getFEN()
        self.engine.load_fen(fen=currentFen)
        
        wtime = self.game.white.time * 1000
        btime = self.game.black.time * 1000
        
        if self.game.constants.next_player == "white":
            _time = wtime
        else:
            _time = btime
            
        # _movestogo -= 1
        _movetime = min(12000, _time // self.movestogo)
        
        # getting best move from the ENGINE
        def calc_best_move():
            self.bestMove = self.engine.best_move()
            
        bestmove_thread = threading.Thread(target=calc_best_move)
        self.engine_running = True
        bestmove_thread.start()
        
        return self.bestMove