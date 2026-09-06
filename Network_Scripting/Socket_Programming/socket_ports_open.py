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