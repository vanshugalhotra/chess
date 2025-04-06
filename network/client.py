import socket
import threading

class ChessClient:
    def __init__(self, host='192.168.1.43', port=65432):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = None
        self.connected = False
        self.latest_move = None  # Store the latest move received from the server
        self.player_id_recieved = threading.Event()
        self.opponent_connected = threading.Event()
        self.score = 0

    def connect(self):
        """Connect to the server."""
        try:
            self.client.connect((self.host, self.port))
            print("Connected to the server.")
            self.connected = True
            threading.Thread(target=self.receive_messages).start()
            
            # self.player_id_recieved.wait()
            if self.player_id is None:
                print('Failed to connect!!!')
                return False
            
        except socket.gaierror:
            raise ConnectionError("Invalid IP Address! Please check and try again.")
        except socket.timeout:
            raise ConnectionError("Connection timed out! Server is not reachable.")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the server: {e}")

    def receive_messages(self):
        """Receive messages from the server."""
        while self.connected:
            try:
                data = self.client.recv(1024).decode('utf-8')
                
                if data.startswith("player_id:"):
                    self.player_id = data.split(':')[1]  # "white" or "black"
                    print(f"You are Player {self.player_id}.")
                elif data == "not_your_turn":
                    print("It's not your turn.")
                elif data == "opponent_connected":
                    print("Opponent Connected!")
                    self.opponent_connected.set()
                else:
                    parts = data.split(':')
                    if len(parts) == 3:
                        move, score, player_id = parts
                        self.latest_move = move
                        self.score = int(score)
                    else:
                        print(f"Received unknown data: {data}")

            except Exception as e:
                print(f"Connection lost: {e}")
                self.connected = False
                break

    def send_move(self, move, score):
        """Send a move to the server."""
        if self.connected:
            try:
                message = f"{move}:{score}:{self.player_id}"
                self.client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to send move: {e}")

