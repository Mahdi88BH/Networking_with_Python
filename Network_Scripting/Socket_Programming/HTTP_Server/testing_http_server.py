import socket


SERVER_IP = 'localhost'
SERVER_PORT = 8080

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:

        so.connect((SERVER_IP, SERVER_PORT))
        print(f"Connecting to Server {SERVER_IP} on port {SERVER_PORT}")

        try:
            so.sendall(bytes("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n".encode('utf-8')))
            response = so.recv(4096)
            print(f"The response are {response.decode('utf-8', errors='ignore')}")

        except KeyboardInterrupt:
            print("\n[*] Shutting down The connection gracefully.")


if __name__ == "__main__":
    main()