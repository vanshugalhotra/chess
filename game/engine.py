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
    
    def analyze(self, cur_fen, depth=3):
        
        eval_before = self.game.constants.prev_score
        eval_after = self.engine.analyze_position(fen=cur_fen, depth=depth)

        score = -(eval_after + eval_before)
        label, color, icon = self._classify_move(score)
        return {
            "before": eval_before,
            "after": eval_after,
            "score": score,
            "classification": label,
            "color": color,
            "icon": icon
        }


        
    @staticmethod
    def _classify_move(score):
        """Classify move and return label, color, and a dot icon"""
        if 0 <= score <= 35:
            return "BEST", (0, 200, 0), "●"  # Green
        elif 35 < score < 100:
            return "EXCELLENT", (34, 139, 34), "●"
        elif -35 <= score < 0:
            return "GOOD", (70, 130, 180), "●"  # Steel Blue
        elif -305 <= score < -35:
            return "MISTAKE", (255, 165, 0), "●"  # Orange
        elif score < -305:
            return "BLUNDER", (220, 20, 60), "●"  # Crimson
        elif 100 < score < 300:
            return "GREAT", (0, 128, 255), "●"
        elif score >= 300:
            return "BRILLIANT", (255, 215, 0), "●"  # Gold
        return "INACCURACY", (128, 128, 128), "●"  # Gray


