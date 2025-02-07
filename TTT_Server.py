import socket

HOST = '127.0.0.1'
PORT = 7654

# Initialize an empty Tic Tac Toe board
def initialize_board():
    return [" " for _ in range(9)]

# Display the board as a string
def display_board(board):
    return f"""
     {board[0]} | {board[1]} | {board[2]}
    ---+---+---
     {board[3]} | {board[4]} | {board[5]}
    ---+---+---
     {board[6]} | {board[7]} | {board[8]}
    """

# Check for a winner
def check_winner(board, mark):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    return any(all(board[pos] == mark for pos in condition) for condition in win_conditions)

# Check for a tie
def check_tie(board):
    return all(cell != " " for cell in board)

# Server's move (simple AI: first available spot)
def computer_move(board):
    for i in range(9):
        if board[i] == " ":
            return i

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server is listening for connections...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            board = initialize_board()
            conn.sendall("Welcome to Tic Tac Toe! You are 'X'. 0 is top left spot; 8 is bottom right.\n".encode())
            conn.sendall(display_board(board).encode())

            while True:
                # Receive the player's move
                try:
                    move = conn.recv(1024).decode()
                    if not move:
                        break

                    move = int(move)  # Convert input to integer (0-8)
                    if board[move] != " ":
                        conn.sendall("Invalid move. Try again.\n".encode())
                        continue

                    # Apply player's move
                    board[move] = "X"

                    # Check if the player wins
                    if check_winner(board, "X"):
                        conn.sendall(f"You win!\n{display_board(board)}".encode())
                        break

                    # Check for a tie
                    if check_tie(board):
                        conn.sendall(f"It's a tie!\n{display_board(board)}".encode())
                        break

                    # Server's move
                    comp_move = computer_move(board)
                    board[comp_move] = "O"
                    conn.sendall(f"Server played position {comp_move}.\n".encode())
                    conn.sendall(display_board(board).encode())

                    # Check if the server wins
                    if check_winner(board, "O"):
                        conn.sendall(f"Server wins!\n{display_board(board)}".encode())
                        break

                    # Check for a tie
                    if check_tie(board):
                        conn.sendall(f"It's a tie!\n{display_board(board)}".encode())
                        break

                except ValueError:
                    conn.sendall("Invalid input. Enter a number between 0 and 8.\n".encode())
                except Exception as e:
                    conn.sendall(f"An error occurred: {e}\n".encode())
                    break

if __name__ == "__main__":
    main()##
