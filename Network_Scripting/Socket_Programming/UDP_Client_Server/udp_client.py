import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6789
TARGET_ADDR = (SERVER_IP, SERVER_PORT)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as so:
        # Set a 2-second timeout on blocking socket operations
        so.settimeout(2.0)
        
        print(f"[*] UDP Client ready. Target: {SERVER_IP}:{SERVER_PORT}")
        print("[*] Type 'quit' or 'exit' to stop.\n")

        while True:
            message = input("Enter your message > ").strip()

            if not message:
                continue

            if message.lower() in ('quit', 'exit'):
                print("[*] Closing UDP client session.")
                break

            try:
                # Transmit datagram to server
                so.sendto(message.encode('utf-8'), TARGET_ADDR)

                # Receive both responses sent by your server (ACK + Response)
                ack, _ = so.recvfrom(4096)
                print(f"[+] Server ACK: {ack.decode('utf-8', errors='ignore')}")

                resp, _ = so.recvfrom(4096)
                print(f"[+] Server Response: {resp.decode('utf-8', errors='ignore')}\n")

            except socket.timeout:
                print("[-] Server timed out (no response received).\n")
            except socket.error as err:
                print(f"[-] Socket error: {err}\n")

if __name__ == "__main__":
    main()