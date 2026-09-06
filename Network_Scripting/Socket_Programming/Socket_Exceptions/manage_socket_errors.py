import socket

host = "domain/ip_address"
port = 80

try:
    # 'with' handles automatic closing of the socket upon exit, even on exception
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
        # Print the raw socket object representation (shows file descriptor, 
        # family, type, and proto).
        print(mysocket)

        # Set a 5-second non-blocking timeout for blocking socket operations 
        # (connect, recv, send).
        # If a connection or response takes longer than 5s, a socket.timeout 
        # exception is raised.
        mysocket.settimeout(5)

        print("Initiating connection...")

        # Initiate the 3-way TCP handshake with (host, port).
        # NOTE: If 'host' is set to literal string "domain/ip_address", 
        # this line triggers socket.gaierror.
        mysocket.connect((host, port))
        print(f"Connected successfully to {host}:{port}")
# Catches connection attempts that exceed the 5-second settimeout() threshold.
except socket.timeout as er:
    print(f"Connection to {host}:{port} timed out after 5 seconds. => {er}")
# Catches Address-related errors (Get Address Information Error), 
# such as invalid hostnames or DNS failures.
except socket.gaierror as er:
    print(f"DNS Resolution failed for host: {host} => {er}")
# Catch-all for other socket-level errors (e.g., ConnectionRefusedError, 
# NetworkUnreachable).
except socket.error as er:
    print(f"Socket connection error: {er}")


# Literal Placeholder ("domain/ip_address"): Triggers socket.gaierror because 
# the OS DNS subsystem cannot resolve domain/ip_address to a valid IP.

# Filtered/Firewalled Host: Triggers socket.timeout after 5 seconds if packets 
# are dropped silently without an RST response.

# Closed Port on Host: Triggers socket.error ([Errno 111] Connection refused 
# on Linux/Kali).

# Open Port ("8.8.8.8" on Port 53 or "google.com" on Port 80): 
# Connects successfully and prints the connected socket details.