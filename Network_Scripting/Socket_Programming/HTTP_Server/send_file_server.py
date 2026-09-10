import socket
import struct


# Helper function to reliably receive exactly 8 bytes (64-bit uint) for file size
def receive_file_size(sock: socket.socket):
    fmt = "<Q" # Little-endian 64-bit unsigned integer
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()

    # Loop guarantees all 8 header bytes are read even if delivered across multiple TCP segments
    while received_bytes < expected_bytes:
        chunk = sock.recv(expected_bytes - received_bytes)

        if not chunk: break

        stream += chunk
        received_bytes += len(chunk)

    # Unpack raw bytes back into an integer; [0] extracts the value from single-element tuple
    filesize = struct.unpack(fmt, stream)[0]

    return filesize


# Receives the raw binary payload and writes it directly to disk
def receive_file(sock: socket.socket, filename):

    filesize = receive_file_size(sock)

    with open(filename, "wb") as f:
        received_bytes = 0

        # Loop until total bytes written equals expected filesize
        while received_bytes < filesize:
            chunk = sock.recv(1024)
            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)
            else:
                break

def main():
    # socket.create_server simplifies socket initialization, sets SO_REUSEADDR, binds, 
    # and calls listen()
    with socket.create_server(("localhost", 9999)) as server:
        print("Waiting the client connection on localhost:9999 ...")
        connection, address = server.accept()

        with connection:
            print(f"{address[0]}:{address[1]} connected.")
            print("Receiving file...")
            receive_file(connection, "./file_received.txt")
            print("File received")


if __name__ == "__main__":
    main()