import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # 2. Establish a 3-way TCP handshake with host 'ftp.debian.org' on HTTP port 80.
# # NOTE : socket.connect expects a single tuple containing (host, port).
# s.connect(('ftp.debian.org', 80))

# # 3. Formulate a raw HTTP/1.0 GET request string and convert (.encode()) it 
# # from str to bytes.
# # Sockets transmit raw bytes, not Python text strings.
# # '\r\n\r\n' (Carriage Return + Line Feed x2) signals the end of the HTTP 
# # request headers.
# cmd = 'GET http://ftp.debian.org/debian/README.mirrors.txt HTTP/1.0\r\n\r\n'.encode()

# # 4. Send the encoded request bytes across the TCP socket to the server.
# nbr_bytes_send = s.send(cmd)
# print(f"Number of Bytes send to a server {nbr_bytes_send}")

# # 5. Loop continuously to receive the incoming response stream from the server.
# while True:
#     # Read up to 512 bytes of data at a time from the socket buffer (blocking call).
#     data = s.recv(512)

#     # When the server finishes sending and closes its end of the connection,
#     # s.recv() returns an empty bytes object (b''), indicating End-Of-File (EOF).
#     if len(data) < 1:
#         break

#     print(data.decode(), end='')

# s.close()


# Modernized Version

# Target connection settings
host = 'ftp.debian.org'
port = 80
path = '/debian/README.mirrors.txt'

# Formulate the HTTP/1.0 request
request = f'GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n'.encode('utf-8')

# Using 'with' handles automatic socket closure, even if an error occurs
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    # sendall guarantees the full buffer is transmitted
    s.sendall(request)

    response_buffer = []

    while True:
        data = s.recv(1024)
        if not data:
            break
        response_buffer.append(data)

# Combine byte chunks and decode the full stream cleanly
full_response = b''.join(response_buffer).decode('utf-8', errors='ignore')
print(full_response)


# NOTE: Partial Send Protection (sendall)
# s.send() is not guaranteed to send all bytes in a single call—it returns 
# the number of bytes actually sent. To ensure the complete request payload 
# is sent over the wire, use s.sendall().

# NOTE: Decoding Multi-Byte UTF-8 Chunks
# When receiving text in arbitrary 512-byte slices (s.recv(512)), 
# a UTF-8 character that spans across the byte boundary can throw a 
# UnicodeDecodeError. Using errors='ignore' or decoding the complete buffer 
# after collecting all bytes prevents crashes.