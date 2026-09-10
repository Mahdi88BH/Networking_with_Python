import ssl
import socket



# def main():

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         # DEPRECATION BUG 1: ssl.wrap_socket() was deprecated in Python 3.7 and REMOVED in Python 3.12!
#         # Calling wrap_socket directly also skips SNI (Server Name Indication) and strict CA validation.
#         secure_socket = ssl.wrap_socket(sock)
#         data = bytearray()

#     # BUG 2: The underlying 'sock' context manager exited above, meaning 'sock' is ALREADY CLOSED here!
#     try:
#         with secure_socket:
#             # Attempts to connect using a wrapper on a closed base socket, raising OSError / Bad file descriptor.
#             secure_socket.connect(("www.google.com", 443))
            
#             # Returns tuple of negotiated cipher parameters: (cipher_name, tls_version, secret_bits)
#             print(secure_socket.cipher())
            
#             # HTTP PROTOCOL BUG 3: HTTP/1.1 request formatting is invalid!
#             # 1. Extra space after path in "GET / HTTP/1.1 ".
#             # 2. HTTP headers MUST end with CRLF (\r\n), NOT single newlines (\n).
#             # 3. Request terminates with \r\n\r\n. Google will return 400 Bad Request or hang.
#             secure_socket.write(b"GET / HTTP/1.1 \r\n")
#             secure_socket.write(b"Host: www.google.com\n\n")
            
#             # BUG 4: read() called once only reads a single buffer chunk (~1-4KB), truncating response.
#             data = secure_socket.read()
#             print(data.decode("utf-8"))
#     except Exception as exception:
#         print("Exception: ", exception)




def main():
    hostname = "www.google.com"
    port = 443

    # 1. Create default secure SSL context (enforces CA validation & modern ciphers)
    context = ssl.create_default_context()

    try:
        # 2. Establish standard TCP connection
        with socket.create_connection((hostname, port)) as raw_sock:
            # 3. Wrap raw TCP socket with TLS, providing server_hostname for SNI support
            with context.wrap_socket(raw_sock, server_hostname=hostname) as tls_sock:
                
                # Print negotiated cipher suite and TLS protocol version
                cipher_info = tls_sock.cipher()
                print(f"[*] TLS Handshake Successful!")
                print(f"[*] Protocol & Cipher: {cipher_info[1]} | {cipher_info[0]} ({cipher_info[2]} bits)\n")

                # 4. Construct RFC 7230 compliant HTTP/1.1 GET Request
                http_request = (
                    f"GET / HTTP/1.1\r\n"
                    f"Host: {hostname}\r\n"
                    f"User-Agent: PythonTLSSocketClient/1.0\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                )

                # Transmit encrypted HTTP request payload
                tls_sock.sendall(http_request.encode('utf-8'))

                # 5. Read complete encrypted response stream
                response_chunks = []
                while True:
                    chunk = tls_sock.recv(4096)
                    if not chunk:
                        break  # Connection closed by server
                    response_chunks.append(chunk)

                full_response = b"".join(response_chunks).decode('utf-8', errors='ignore')
                print("=== ENCRYPTED HTTPS RESPONSE RECEIVED ===")
                print(full_response[:500] + "\n... [truncated]")

    except ssl.SSLError as ssl_err:
        print(f"[-] TLS Verification/Handshake Error: {ssl_err}")
    except socket.error as sock_err:
        print(f"[-] Socket/Network Error: {sock_err}")


if __name__ == "__main__":
    main()