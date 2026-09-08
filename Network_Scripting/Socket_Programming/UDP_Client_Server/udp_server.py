import sys
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6789


def main():

    # 1. Instantiate an IPv4 (AF_INET), UDP (SOCK_DGRAM) datagram socket using context manager.
    # Unlike TCP (SOCK_STREAM), UDP is connectionless and message-oriented.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as so:
        # 2. Bind the UDP socket to the local host address and port to listen for incoming datagrams.
        so.bind((SERVER_IP, SERVER_PORT))

        print(f"[*] UDP Server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            # 3. Read up to 4096 bytes from the UDP socket buffer.
            # Returns a 2-element tuple: (data_bytes, client_address_tuple).
            data, addr = so.recvfrom(4096)
            so.sendto(
                f"Server ACK: Received from IP {addr[0]} port {addr[1]}".encode('utf-8'), 
                addr
            )

            data = data.decode('utf-8', errors='ignore').strip()

            print(f"[*] Received message from {addr[0]}:{addr[1]} => '{data}'")

            try:
                response = f"Hi from server running on {sys.platform}"
            except KeyboardInterrupt:
                print("\n[*] Server shutting down gracefully.")
                break
            except Exception as ex:
                response = f"{sys.exc_info()[0]}"

            print(f"[*] Sending Response: {response}")
            so.sendto(response.encode('utf-8'), addr)


if __name__ == "__main__":
    main()