import sys
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6789


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as so:
        so.bind((SERVER_IP, SERVER_PORT))
        print(f"[*] UDP Server listening on {SERVER_IP}:{SERVER_PORT}")
        print("[*] Press Ctrl+C to stop the server safely.\n")

        try:
            while True:
                # Wait for incoming datagram
                data, addr = so.recvfrom(4096)

                # Send ACK packet
                ack_msg = f"Server ACK: Received from IP {addr[0]} port {addr[1]}"
                so.sendto(ack_msg.encode('utf-8'), addr)

                payload = data.decode('utf-8', errors='ignore').strip()

                if payload.lower() == 'quit':
                    print(f"[*] Client {addr[0]}:{addr[1]} sent 'quit'. Ending server session.")
                    so.sendto(b"Server session terminated.\n", addr)
                    break

                print(f"[*] Message from {addr[0]}:{addr[1]} => '{payload}'")

                # Prepare platform response
                response = f"Hi from server running on {sys.platform}"
                print(f"[*] Sending Response: {response}")
                
                so.sendto(response.encode('utf-8'), addr)

        except KeyboardInterrupt:
            print("\n[*] Server shutting down gracefully (KeyboardInterrupt).")
        except socket.error as err:
            print(f"[-] Socket error encountered: {err}")


if __name__ == "__main__":
    main()