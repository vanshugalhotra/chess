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
    
    def analyze(self, cur_fen):
        
        eval_before = self.game.constants.prev_score
        eval_after = self.engine.analyze_position(fen=cur_fen)

        score = -(eval_after + eval_before)
        move_classification = self._classify_move(score)
        
        # print(f'{"white" if self.game.constants.next_player == "black" else "black"} moved ::: Score went from {eval_before}  --> {-eval_after} ::: score: {score}')

        return {
            "before": eval_before,
            "after": eval_after,
            "score": score,
            "classification": move_classification
        }
        
    @staticmethod
    def _classify_move(score):
        """Classify move based solely on score"""
        if(score >= 0 and score <= 35):
            return "BEST"
        elif(score > 35 and score < 100):
            return "EXCELLENT"
        elif(score < 0 and score >= -35):
            return "GOOD"
        elif(score < -35 and score >= -305):
            return "MISTAKE"
        elif(score < -305):
            return "BLUNDER"
        elif(score > 100 and score < 300):
            return "GREAT"
        elif(score >= 300):
            return "BRILLIANT"
        return "INACCURACY"
