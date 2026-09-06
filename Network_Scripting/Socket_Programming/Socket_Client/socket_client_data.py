import socket

host = input("Enter host name: ").strip()
port = int(input("Enter port number: "))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
        socket_tcp.settimeout(10)
        
        status = socket_tcp.connect_ex((host, port))
        
        if status != 0:
            print(f"Port {port} on {host} is CLOSED or FILTERED (Error Code: {status})")
        else:
            print(f"Connected successfully to {host}:{port}")
            
            # Standardized HTTP/1.1 GET request with 'Connection: close'
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            socket_tcp.sendall(request.encode('utf-8'))
            
            # Read complete incoming response payload
            response_chunks = []
            while True:
                chunk = socket_tcp.recv(4096)
                if not chunk:
                    break
                response_chunks.append(chunk)
            
            full_data = b"".join(response_chunks)
            print(f"\n--- Output (Received {len(full_data)} bytes) ---")
            print(full_data.decode('utf-8', errors='ignore'))

# Catches socket operations exceeding the 10-second timeout threshold.
except socket.timeout:
    print("Connection attempt timed out.")

# Catches DNS name resolution failures (e.g., unresolvable hostname).
except socket.gaierror as error:
    print(f"DNS Resolution failed for host '{host}': {error}")

# Catch-all for lower-level socket/OS network exceptions.
except socket.error as error:
    print(f"Network error occurred: {error}")




# Key Operational Issues & Improvements

# 1. connect_ex() Non-Zero Behavior:
# If connect_ex() fails (returns non-zero code like 111 or 10061), the 
# if condition evaluates to False. The script simply exits the with block 
# silently without printing any output or warning that the port was closed.

# 2. HTTP Request Format:
# HTTP/1.1 requires a space between Host: and the hostname (Host: {host}). 
# While some servers parse Host:{host}, standard compliance requires 
# Host: {host}.

# 3. send vs sendall:
# socket.send() does not guarantee sending the entire byte buffer in one pass.
# Using socket.sendall() forces Python to loop internally until all bytes 
# are transmitted.

# 4. Handling Partial Responses:
# recv(4096) only fetches the first packet chunk up to 4KB. HTTP responses 
# (headers + HTML body) often exceed 4KB. Reading inside a loop collects 
# the full response stream until EOF (b"").