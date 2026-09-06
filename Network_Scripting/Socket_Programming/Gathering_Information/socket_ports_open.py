# - The main socket methods :
#     • socket.accept() is used to accept connections and returns a value pair 
#     as (conn, address).
#     • socket.bind() is used to bind addresses specified as a parameter.
#     • socket.connect() is used to connect to the address specified as a parameter.
#     • socket.listen() is used to listen for commands on the server or client.
#     •socket.recv(buflen) is used for receiving data from the socket. The method 
#     argument indicates the maximum amount of data it can receive.
#     • socket.recvfrom(buflen) is used for receiving data and the sender’s 
#     address.
#     • socket.recv_into(buffer) is used for receiving data into a buffer.
#     • socket.send(bytes) is used for sending bytes of data to the specified 
#     target.
#     • socket.sendto(data, address) is used for sending data to a given address.
#     • socket.sendall(data) is used for sending all the data in the buffer to 
#     the socket.
#     • socket.close() is used for releasing the memory and finishes 
#     the connection.
    

import socket


ip ='127.0.0.1'
portlist = [21,22,23,80]

if __name__ == "__main__":
    for port in portlist:
        # Create an IPv4 (AF_INET), TCP (SOCK_STREAM) socket instance.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0) # Set 1 second connection timeout

        # connect_ex() attempts to connect to (ip, port).
        # Unlike s.connect(), connect_ex() does NOT throw an exception on failure.
        # It returns an error indicator:
        #   0    == Success (Port is OPEN)
        #   111  == Connection Refused / Closed (Linux/macOS)
        #   10061 == Connection Refused / Closed (Windows)
        result = s.connect_ex((ip, port))

        if result == 0:
            print(f"Port {port}: OPEN")
        else:
            print(f"Port {port}: CLOSED/FILTERED (Code: {result})")

        s.close()


# NOTE :Missing Socket Timeout: 
# By default, socket.connect_ex() uses the system's default TCP connection 
# timeout (which can take up to 20–120 seconds per closed/filtered port on 
# remote hosts). Adding s.settimeout(1.0) forces the scanner to move on 
# quickly if a port drops or filters packets.