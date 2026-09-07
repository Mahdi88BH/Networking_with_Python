import socket

host = '127.0.0.1'
port = 9999


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
            so.connect((host, port))
            print(f"[*] Connected to server at {host}:{port}")

            # Receive initial welcome banner from the server
            banner = so.recv(1024)
            print(f"[*] Banner: {banner.decode('utf-8').strip()}")

            while True:
                request = input("Enter request (or 'quit' to exit): ").strip()
                
                if not request:
                    continue  # Don't send empty strings

                # Send message to server
                so.sendall(request.encode('utf-8'))

                if request.lower() == 'quit':
                    print("[*] Terminating connection session.")
                    break

                # Read ACK or server response message back
                ack = so.recv(1024)
                if not ack:
                    print("[-] Server closed the connection unexpectedly.")
                    break

                print(f"[*] Server Response: {ack.decode('utf-8').strip()}")

    except socket.error as error:
        print(f"[-] Socket error encountered: {error}")


if __name__ == "__main__":
    main()