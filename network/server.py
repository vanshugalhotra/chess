import socket
import threading
import json
import random

HOST = '127.0.0.1'  
PORT = 65432        
clients = {} 
turn = None  

def handle_client(conn, player_id):
    global turn

    print(f"Player {player_id} connected.")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            move_data = json.loads(data)

            # Enforce turn-based gameplay
            if move_data["player_id"] != turn:
                conn.sendall(json.dumps({"error": "Not your turn!"}).encode())
                continue

            print(f"Received move: {move_data}")

            # Switch turn
            turn = 1 if turn == 2 else 2

            # Relay move to the other player
            for client, pid in clients.items():
                if client != conn:
                    client.sendall(json.dumps(move_data).encode())

        except (ConnectionResetError, json.JSONDecodeError):
            break

    print(f"Connection closed: Player {player_id}")
    del clients[conn]
    conn.close()

def start_server():
    global turn

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"Server started on {HOST}:{PORT}, waiting for players...")

    # Assign random colors
    player_ids = [1, 2]  # 1 = White, 2 = Black
    random.shuffle(player_ids)

    while len(clients) < 2:
        conn, addr = server.accept()
        player_id = player_ids.pop()
        clients[conn] = player_id

        # Send assigned player ID
        conn.sendall(json.dumps({"player_id": player_id}).encode())

        threading.Thread(target=handle_client, args=(conn, player_id)).start()

    # Set White (Player 1) to move first
    turn = 1

if __name__ == "__main__":
    start_server()
