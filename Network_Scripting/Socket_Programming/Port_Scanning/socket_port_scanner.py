import sys
from datetime import datetime
import socket




def reverse_dns_lookup(remote_host):
    """Implement a reverse DNS lookup to get The IP Address"""

    try:
        return socket.gethostbyname(remote_host)
    except socket.gaierror:
        print(f"[-] Could not resolve hostname: {remote_host}")
        sys.exit(1)


def get_port_by_name(port):
    """get The Name of a port by his name"""
    try:
        return socket.getservbyport(port, 'tcp')
    except (OSError, socket.error):
        return "unknow"


def main():
    target = input("Please entre a remote host : ").strip()

    print("Please Entre a range of port (ex: start port, end port) ")
    try:
        start_port = int(input("start port : "))
        end_port =int(input("end port :"))
    except ValueError:
        print("[-] Invalid Port Number")
        sys.exit(1)


    init_time = datetime.now()
    print("The Scanning is starting .....")

    ip_addr = reverse_dns_lookup(target)

    for port in range(start_port, end_port + 1):
        print(f"Targeting the port {get_port_by_name(port)} {port}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
            
                res = s.connect_ex((ip_addr, port))
            
                if res == 0:
                    print("[+] The port is Up")
                else:
                    print("[-] The port is CLOSED/FILTRED")
        except KeyboardInterrupt:
            print("Presse Ctrl+c")
            sys.exit(0)
        except socket.gaierror:
            print("We Could Not connect to ther Server ")
            sys.exit(1)

    end_time = datetime.now()
    total = end_time - init_time

    print(f"The Scan are Completed at {total}")


if __name__ == "__main__":
    main()