import os
import struct
import socket


def send_file(sock: socket.socket, filename):
    # Retrieve total size of target file in bytes for the binary header frame
    file_size = os.path.getsize(filename=filename)

    with sock:
        # Pack 64-bit unsigned integer (8 bytes, little-endian '<Q') representing file size 
        # and send header
        sock.sendall(struct.pack("<Q", file_size))

        # Open file in binary read mode ('rb') to preserve raw byte data (executables, images, text)
        with open(filename, 'rb') as f:

            # Chunked file streaming loop using Python 3.8+ walrus operator (:=)
            while read_bytes := f.read(1024):
                sock.sendall(read_bytes)


def main():

    # Helper function 'create_connection' performs both socket creation and connect() in one step
    with socket.create_connection(('localhost', 9999)) as conn:
        print("Connecting with server ....")
        print("Sending File ......")
        send_file(conn, "./file_sended.txt")

        print("File sended")


if __name__ == "__main__":
    main()