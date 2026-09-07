import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Allow immediate socket reuse to prevent "Address already in use" errors
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to local IP and Port
        server.bind((SERVER_IP, SERVER_PORT))

        # Place socket in passive listening mode with a backlog queue of 5 connections
        server.listen(5)

        print(f"[*] Server listening on {SERVER_IP}:{SERVER_PORT}")

        # Blocking call: waits for an incoming client connection.
        # Returns a new client socket object and a tuple containing (client_ip, client_port)
        client, addr = server.accept()

        with client:
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

            # Send initial welcome banner to the client upon connection
            client.sendall(f"Am the Server Accepting connections on posrt : {SERVER_PORT}".encode("utf-8"))

            while True:
                data = client.recv(1024)

                if not data:
                    break

                request = data.decode('utf-8').strip()
                print(f"[*] Recived Request : {request}")

                if request.lower() == 'quite':
                    print("[*] Client requested termination. Closing session.")
                    break

                # Send acknowledgement back to client
                client.sendall(b"ACK\n")


if __name__ == "__main__":
    main()