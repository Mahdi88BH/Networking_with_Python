import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def socket_scan(host, port):
    """test single conectivity TCP Port"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            res = s.connect_ex((host, port))
            if res == 0:
                return port, True, "OPEN"
            return port, False, "CLOSED/FILTERED"
    except socket.error as er:
        return port, False, f"ERROR ({er})"


def parse_ports(port_str):
    """Parse comma-seperated ports and renage (e.g 22,80,100-105) into integers"""
    ports = set()

    for p in port_str.split(','):
        if '-' in p:
            start, end = p.split('-')
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(p))

    return sorted(list(ports))



def port_scanning(host, ports, max_workers=3):
    """Resolves Target DNS and manage thread pool execution"""

    try:
        ip_addr = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[-] Could not resolve hostname : {host}")

    try:
        name = socket.gethostbyaddr(ip_addr)[0]
        print(f"[+] Target: {host} ({ip_addr}) [rDNS : {name}]")
    except socket.herror:
        print(f"[+] Target: {host} ({ip_addr})")

    print(f"Scanning {len(ports)} using {max_workers} Thread .......\n")

    start_time = datetime.now()


    with ThreadPoolExecutor(max_workers=max_workers) as th:
        futures = {th.submit(socket_scan, ip_addr, port) : port for port in ports}

        for future in as_completed(futures):
            port, is_open, status = future.result()

            if is_open:
                print(f"[+] Port {port} : {status}")
            else:
                print(f"[-] Port {port} : {status}")

    duration = datetime.now() - start_time
    print(f"\n[+] Scan Completed in {duration}")



def main():
    parser = argparse.ArgumentParser(
        description='MultiThread TCP Port Scann'
    )

    parser.add_argument(
        '--H', '-host',
        dest='host',
        help='Target hostname or IP',
        required=True
    )

    parser.add_argument(
        '--P', '-ports',
        dest='ports',
        help='Target range of ports',
        required=True
    )

    parser.add_argument(
        '--T', '-threads',
        dest='thread',
        type=int,
        default=3,
        help='Number of concurrent worker threads (default: 3)'
    )


    args = parser.parse_args()

    try:
        ports = parse_ports(args.ports)
    except ValueError:
        print("[-] Invalid port specification. Use numbers or ranges like '22,80-100'.")
        return

    port_scanning(args.host, ports, 3)



if __name__ == "__main__":
    main()