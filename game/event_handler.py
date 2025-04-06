import pygame
import sys
from const import SQSIZE
from game import Move, Square
from network import ChessClient
from .input_popup import IPInputPopup

class EventHandler:
    def __init__(self, game, screen, engine):
        self.game = game
        self.board = self.game.board
        self.dragger = self.game.dragger
        self.screen = screen
        self.play_button = None
        
        self.mode = 1 # single player - 1, multiplayer - 2
        self.client = None
        self.engine = engine

        self.spinner_angle = 0
        
    def connect_client(self):
        self.mode = 2  # Multiplayer mode
        self.reset()
        
        if not hasattr(self, 'ip_popup'):
            self.ip_popup = IPInputPopup(self.screen) 
        
        self.ip_popup.show()
        connecting = False
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                result = self.ip_popup.handle_event(event)
                if result == "cancel":
                    self.ip_popup.hide()
                    print("Exiting...")
                    exit()
                elif result is not None and not connecting:
                    ip = result
                    connecting = True
                    
                    try:
                        self.client = ChessClient(host=ip)
                        self.client.connect()
                        self.ip_popup.set_success(f"Connected successfully! Player ID: {self.client.player_id}")
                        
                        # Set flip_board based on player_id
                        self.game.flip_board = self.client.player_id == "black"
                        pygame.time.delay(1500)  # Show success message for 1.5 seconds
                        self.ip_popup.hide()
                        return  # Exit the connection process
                        
                    except Exception as e:
                        self.ip_popup.set_error(f"Failed to connect: {str(e)}")
                        connecting = False
            
            # Your normal game rendering here
            self.screen.fill((255, 255, 255))  # Clear screen
            # ... draw your chess board and pieces ...
            
            # Draw the popup on top
            self.ip_popup.draw()
            
            pygame.display.flip()

        
    def set_play_button(self, play_button):
        self.play_button = play_button
        
    def handle_events(self):
        if(self.mode == 2 and self.client):
            self.check_for_opponent_move()
            
            if not self.client.opponent_connected.is_set():
                self.spinner_angle = self.game.show_popup(
                self.screen,
                text="Waiting for opponent...",
                animation_type="spinner",
                angle=self.spinner_angle
                )
                pygame.time.delay(100)
            
            else:                    
                if not hasattr(self, "game_start_popup_shown"):
                    opponent_id = "black" if self.client.player_id == "white" else "white"
                    for i in range(3, 0, -1):
                        self.game.show_popup(
                            self.screen,
                            text=f"Starting in {i}...",
                        )
                        pygame.time.delay(1000)  # 1-second delay for countdown
                    
                    self.game.show_popup(
                        self.screen,
                        text=f"Game started! Your opponent is Player {opponent_id}",
                        animation_type="tick"
                    )
                    pygame.time.delay(2000)  # Small delay before game starts
                    self.game_start_popup_shown = True
                    self.game.start_game()

            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if self.mode == 2 and self.client and not self.client.opponent_connected.is_set():
                continue 
            
            if not self.board.checkmate and not self.board.repetition:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_button_up(event)
                
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    
    def handle_mouse_button_down(self, event):
        if event.button == 4:
            self.game.scroll_y -= 15
        elif event.button == 5:
            self.game.scroll_y += 15
        
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_button.collidepoint(mouse_pos):
                self.game.start_game()
        
        if not self.game.start:
            return
        
        if self.mode == 2 and self.client.player_id != self.game.constants.next_player:
            return
        
        self.dragger.update_mouse(event.pos)
        clicked_row, clicked_col = self.dragger.mouseY // SQSIZE, self.dragger.mouseX // SQSIZE
        
        # Calculate the row and column based on flip_board
        if self.game.flip_board:
            clicked_row, clicked_col = 7 - clicked_row, 7 - clicked_col
        
        if Square.in_range(clicked_row, clicked_col):
            if self.board.squares[clicked_row][clicked_col].has_piece():
                piece = self.board.squares[clicked_row][clicked_col].piece
                if piece.color == self.game.constants.next_player:
                    self.board.calc_moves(piece, clicked_row, clicked_col, wannaCheck=True)
                    self.dragger.save_initial(event.pos)
                    self.dragger.drag_piece(piece)
                    self.update_board()
    
    def handle_mouse_motion(self, event):
        motion_row, motion_col = event.pos[1] // SQSIZE, event.pos[0] // SQSIZE
        self.game.set_hover(motion_row, motion_col)
        
        if self.dragger.dragging:
            self.dragger.update_mouse(event.pos)
            self.update_board()
            self.game.show_hover(self.screen)
            self.dragger.update_blit(self.screen)
    
    def handle_mouse_button_up(self, event):
        if self.dragger.dragging:
            self.dragger.update_mouse(event.pos)
            released_row, released_col = self.dragger.mouseY // SQSIZE, self.dragger.mouseX // SQSIZE
            
            initial_row, initial_col = self.dragger.initial_row, self.dragger.initial_col
            
            if self.game.flip_board:
                released_row, released_col = 7 - released_row, 7 - released_col
                initial_row, initial_col = 7 - initial_row, 7 - initial_col
            

            move = Move(Square(initial_row, initial_col),
                        Square(released_row, released_col))
            if move.is_valid(self.dragger.piece):
                captured = self.board.squares[released_row][released_col].has_piece()
                
                self.board.make_move(self.dragger.piece, move)
                self.game.play_sound(captured)
                self.update_board()
                
                alg_move = move.initial.get_notation()
                alg_move += move.final.get_notation()
                
                
                self.game.next_turn()
                score = 0
                
                if(self.game.analysis):
                    cur_fen = self.board.getFEN()
                    move_analysis = self.engine.analyze(cur_fen=cur_fen)
                    if(self.mode != 2):
                        self.game.constants.prev_score = move_analysis["after"]
                    
                    score = move_analysis["after"]
                    
                    self.game.last_move_info = {
                        "square": (released_row, released_col),
                        "score": move_analysis["score"],
                        "classification": move_analysis["classification"],
                        "icon": move_analysis["icon"],
                        "color": move_analysis["color"],
                        "time": pygame.time.get_ticks()
                    }
                    
                    print(f"{move_analysis['before']} ---> {move_analysis['after']} ::: {move_analysis['score']}")

                if(self.mode == 2):
                    self.client.send_move(alg_move, score)
                
            else:
                self.dragger.piece.clear_moves()
        
        self.dragger.undrag_piece()
        
    def reset(self):
        self.game = self.game.reset()
        self.board = self.game.board
        self.dragger = self.game.dragger
    
    def handle_key_down(self, event):
        if event.key == pygame.K_t:
            self.game.change_theme()
        elif event.key == pygame.K_r:
            self.reset()
            self.game.display_message(self.screen, "Reseted!!")
        elif event.key == pygame.K_m and self.mode != 2:
            self.game.toggle_engine_mode()
            self.game.display_message(self.screen, "Changed Mode!!!")
        elif event.key == pygame.K_p:
            self.game.start_game()
            self.game.display_message(self.screen, "Play!!")
        elif event.key == pygame.K_c:
            self.game.display_message(self.screen, "Connecting....")
            self.connect_client()
        elif event.key == pygame.K_a:
            mode = self.game.toggle_analysis()
            self.game.display_message(self.screen, f"ANALYSIS MODE: {mode}")
    
    def update_board(self):
        self.game.update_screen(self.screen)
        
    def check_for_opponent_move(self):
        """Check if an opponent's move has arrived and apply it."""
        if self.client.connected:
            # Fetch the latest move from the client
            if hasattr(self.client, 'latest_move') and self.client.latest_move:
                move_str = self.client.latest_move
                print(f"Applying opponent's move: {move_str}")

                # Apply the move to the game
                self.game.make_move(move_str)
                self.update_board()
                self.game.next_turn()
                
                self.game.constants.prev_score = self.client.score

                # Clear the latest move to avoid reprocessing
                self.client.latest_move = None
