from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


# # Custom request handler inheriting from standard BaseHTTPRequestHandler
# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         # Transmit HTTP 200 OK status code header
#         self.send_response(200)
#         # Write standard CRLF header terminator line (\r\n)
#         self.end_headers()
#         # Write binary string response payload back to the client
#         self.wfile.write(b'Hello, world!')

# if __name__ == '__main__':

#     # Initialize standard TCP HTTP server listening on localhost:4443
#     https_server = HTTPServer(('localhost', 4443), SimpleHTTPRequestHandler)
    
#     # DEPRECATION BUG 1: ssl.Purpose.CLIENT_AUTH is intended for authenticating CLIENTS (mutual TLS / mTLS).
#     # For a server validating itself to clients, use ssl.Purpose.SERVER_AUTH (or ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)).
#     context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
#     # Load public certificate (cert.pem) and private key (key.pem) into the SSL context
#     context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    
#     # DEPRECATION BUG 2: Direct assignment to https_server.socket via wrap_socket is deprecated.
#     # In modern Python, wrapping the socket before binding/listening or using SSLContext.wrap_socket on the server socket is preferred.
#     https_server.socket = context.wrap_socket(https_server.socket, server_side=True)
    
#     # Start blocking event loop to handle incoming HTTPS requests indefinitely
#     https_server.serve_forever()




class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'Hello, world! Secure HTTPS connection established.'
        
        # Send HTTP Response Headers
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        
        # Write Body
        self.wfile.write(body)


def main():
    host = 'localhost'
    port = 4443

    # 1. Instantiate dedicated server-side SSL context (TLS 1.2/1.3)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # 2. Load self-signed or CA-issued certificate pair
    try:
        context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    except FileNotFoundError:
        print("[-] Error: 'cert.pem' or 'key.pem' not found in current directory.")
        print("[*] Generate them using: openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365")
        return

    # 3. Create HTTP Server instance
    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    
    # 4. Wrap raw server listening socket with TLS context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"[*] Serving HTTPS on https://{host}:{port} ...")
    print("[*] Press Ctrl+C to stop the server.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server shutting down gracefully.")
        httpd.server_close()

if __name__ == '__main__':
    main()