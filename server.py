import socket
import threading
import time
from control_info import build_packet

board = [str(i) for i in range(1, 10)]
current_player = "X"
players = []
lock = threading.Lock()
game_started = False

def print_board():
    return f"""
 {board[0]} | {board[1]} | {board[2]}
---+---+---
 {board[3]} | {board[4]} | {board[5]}
---+---+---
 {board[6]} | {board[7]} | {board[8]}
"""

def is_winner():
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(board[a]==board[b]==board[c] for a,b,c in wins)

def is_draw():
    return all(cell in ["X","O"] for cell in board)

def broadcast(message):
    packet = build_packet(message, "CRC16")
    for p in players:
        p.sendall(packet.encode())

def reset_game():
    global board, current_player
    board = [str(i) for i in range(1, 10)]
    current_player = "X"

def handle_client(client, symbol):
    global current_player, game_started

    client.sendall(build_packet(f"Welcome Player {symbol}", "CRC16").encode())

    while len(players) < 2:
        pass

    if not game_started:
        game_started = True
        broadcast("Both players connected")
        broadcast(print_board())

    while True:
        try:
            with lock:
                if current_player == symbol:
                    client.sendall(build_packet("Enter cell number:", "CRC16").encode())
                    move = client.recv(1024).decode().split("|")[0]

                    if move.isdigit() and int(move) in range(1,10) and board[int(move)-1] not in ["X","O"]:
                        board[int(move)-1] = symbol
                        broadcast(print_board())

                        if is_winner():
                            broadcast(f"Player {symbol} wins")
                            time.sleep(2)
                            reset_game()
                            broadcast("Game restarted")
                            broadcast(print_board())
                            break

                        if is_draw():
                            broadcast("Draw")
                            time.sleep(2)
                            reset_game()
                            broadcast("Game restarted")
                            broadcast(print_board())
                            break

                        current_player = "O" if current_player=="X" else "X"
                    else:
                        client.sendall(build_packet("Invalid move", "CRC16").encode())
                else:
                    client.sendall(build_packet("Waiting for other player...", "CRC16").encode())
        except:
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen(2)

    print("Server started...")
    while len(players) < 2:
        client, addr = server.accept()
        players.append(client)
        symbol = "X" if len(players)==1 else "O"
        threading.Thread(target=handle_client, args=(client,symbol)).start()

if __name__== '__main__':
    main()