import socket
import threading

class ChessServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(2)  # Allow only 2 players to connect
        self.clients = []  # List to store client connections
        self.player_ids = {}  # Dictionary to map player IDs to clients
        self.current_turn = "white"  # Player 0 (White) starts first
        self.game_over = False

    def broadcast(self, message, sender=None):
        """Send a message to all connected clients except the sender."""
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.clients.remove(client)

    def handle_client(self, client):
        """Handle communication with a connected client."""
        player_id = "white" if len(self.player_ids) == 0 else "black"  # Assign "white" or "black"
        self.player_ids[client] = player_id
        client.send(f"player_id:{player_id}".encode('utf-8'))  # Send player ID to client

        print(f"Player {player_id} connected.")
        
        if len(self.clients) == 2:
            for c in self.clients:
                c.send("opponent_connected".encode('utf-8'))

        while not self.game_over:
            try:
                data = client.recv(1024).decode('utf-8')
                if not data:
                    break

                move, player_id = data.split(':')
                if player_id == self.current_turn:
                    print(f"Player {player_id} made move: {move}")
                    self.broadcast(data, sender=client)  # Send move to other player
                    self.current_turn = "black" if self.current_turn == "white" else "white"  # Switch turns
                else:
                    client.send("not_your_turn".encode('utf-8'))  # Notify client it's not their turn
            except Exception as e:
                print(f"Error: {e}")
                break

        client.close()
        self.clients.remove(client)
        print(f"Player {player_id} disconnected.")
        if len(self.clients) == 0:
            self.game_over = True

    def start(self):
        """Start the server and accept client connections."""
        print("Server started. Waiting for players...")
        while len(self.clients) < 2:
            client, addr = self.server.accept()
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

        print("Game started. Player (White) goes first.")

if __name__ == "__main__":
    server = ChessServer()
    server.start()