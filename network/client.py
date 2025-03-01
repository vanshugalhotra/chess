import socket
import threading
import json

HOST = '127.0.0.1'  
PORT = 65432        

class ChessClient:
    def __init__(self):
        """Initialize client and connect to server."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        
        # Receive assigned player ID
        data = self.client.recv(1024).decode()
        self.player_id = json.loads(data)["player_id"]
        
        self.my_turn = (self.player_id == 1)  # White starts first
        color = "White" if self.player_id == 1 else "Black"
        print(f"You are Player {self.player_id} ({color}). Waiting for your turn.")

        # Start listening for opponent's moves
        threading.Thread(target=self.receive_moves, daemon=True).start()

    def send_move(self, move):
        """Send a move if it's the player's turn."""
        if not self.my_turn:
            print("Not your turn! Wait for the opponent.")
            return

        move_data = json.dumps({"player_id": self.player_id, "move": move})
        self.client.sendall(move_data.encode())

        # Wait for opponent's move
        self.my_turn = False

    def receive_moves(self):
        """Receive opponent's moves and update turn."""
        while True:
            try:
                data = self.client.recv(1024).decode()
                if data:
                    move_data = json.loads(data)

                    if "error" in move_data:
                        print(move_data["error"])  # Show error if move was out of turn
                        continue

                    color = "White" if move_data["player_id"] == 1 else "Black"
                    print(f"{color} ({move_data['player_id']}) moved: {move_data['move']}")

                    # It's now my turn
                    if move_data["player_id"] != self.player_id:
                        self.my_turn = True
                        print("Your turn!")

            except (ConnectionResetError, json.JSONDecodeError):
                print("Connection lost.")
                break

if __name__ == "__main__":
    player = ChessClient()
    
    while True:
        move = input("Enter move (e.g., e2e4): ")
        player.send_move(move)
