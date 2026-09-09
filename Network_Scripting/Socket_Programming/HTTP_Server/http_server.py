import socket


HTTP_SERVER_IP = 'localhost'
HTTP_SERVER_Port = 8080

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
        # Allow immediate port reuse upon server restart
        so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        so.bind((HTTP_SERVER_IP, HTTP_SERVER_Port))
        so.listen(5)

        try:
            while True:
                print("Waiting for connections!")
                rcvSocket, addr = so.accept()
                with rcvSocket:
                    print(f"The request recived from {addr[0]}:{addr[1]} are : {rcvSocket.recv(1024).decode('utf-8', errors='ignore')}")
                    rcvSocket.sendall(
                        bytes("HTTP/1.1 200 OK\r\n\r\n <html><body><h1>Hello World!</h1></body></html> \r\n",'utf-8')
                        )
        except KeyboardInterrupt:
            print("\n[*] Shutting down HTTP server gracefully.")

if __name__ == "__main__":
    main()