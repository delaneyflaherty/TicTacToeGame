import socket

HOST = '127.0.0.1'
PORT = 7654

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to the Tic Tac Toe server.")

            while True:
                # Receive and print the server's message
                message = s.recv(1024).decode()
                print(message)

                if "win" in message.lower() or "tie" in message.lower():
                    print("Game over!")
                    break

                # Get user input for the next move
                move = input("Enter your move (0-8): ").strip()
                s.sendall(move.encode())

        except ConnectionRefusedError:
            print("Connection was refused. Make sure the server is running.")
        except KeyboardInterrupt:
            print("\nClient interrupted. Exiting...")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()##
