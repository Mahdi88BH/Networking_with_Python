# ==============================Socket Methods=============================
# • socket.gethostbyname(hostname): This method returns a string converting 
# a hostname to the IPv4 address format. This method is equivalent to 
# the nslookup command we can find in some operating systems.

# • socket.gethostbyname_ex(name): This method returns a tuple that contains 
# an IP address for a specific domain name. If we see more than one IP address, 
# this means one domain runs on multiple IP addresses:

# • socket.getfqdn([domain]): This is used to find the fully qualified name of 
# a domain.

# • socket.gethostbyaddr(ip_address): This method returns a tuple with three values 
# (hostname, name, ip_address_list). hostname represents the host that corresponds 
# to the given IP address, name is a list of names associated with this IP address, 
# and ip_address_list is a list of IP addresses that are available on 
# the same host.

# • socket.getservbyname(servicename[, protocol_name]): This method allows you 
# to obtain the port number from the port name.

# • socket.getservbyport(port[, protocol_name]): This method performs the reverse 
# operation to the previous one, allowing you to obtain the port name from 
# the port number.


import socket

try:
    # 1. Retrieve the local host system name (e.g., 'ubuntu-desktop' or 
    # 'MacBook-Pro').
    hostname = socket.gethostname()
    print("gethostname:",hostname)

    # 2. Resolve the local hostname to its associated IPv4 loopback or LAN IP.
    ip_address = socket.gethostbyname(hostname)
    print("Local IP address: %s" %ip_address)

    # 3. Resolve a remote domain name to a single primary IPv4 address.
    print("gethostbyname:",socket.gethostbyname('www.python.org'))

    # 4. Resolve domain name and return a tuple: (canonical_name, alias_list, 
    # ip_address_list).
    # Useful for load-balanced targets served by multiple IPs.
    print("gethostbyname_ex:",socket.gethostbyname_ex('www.python.org'))

    # 5. Perform a Reverse DNS (rDNS) lookup to map an IP address back to its 
    # PTR hostname record.
    print("gethostbyaddr:",socket.gethostbyaddr('8.8.8.8'))

    # 6. Retrieve the Fully Qualified Domain Name (FQDN) for a target domain.
    print("getfqdn:",socket.getfqdn('www.google.com'))

    # 7. Low-level address translation returning a list of 5-tuples needed 
    # to open socket connections.
    # Returns (family, type, proto, canonname, sockaddr) for IPv4/IPv6 
    # compatibility.
    print("getaddrinfo:",socket.getaddrinfo(
        "www.google.com", 
        None, 
        0, 
        socket.SOCK_STREAM))
# Catch network-related errors (DNS resolution failures, unreachable hosts, 
# socket errors).
except socket.error as error:
    print (str(error))
    print ("Connection error")


# NOTE 1. Modern Practice: Prefer getaddrinfo over gethostbyname
# socket.gethostbyname() is limited to IPv4 addresses only. In dual-stack 
# environments supporting both IPv4 and IPv6, modern socket programming uses 
# socket.getaddrinfo(). It returns family details (AF_INET or AF_INET6), 
# allowing your tools to handle both protocols seamlessly.

# NOTE 2. Reverse DNS Timeouts
# Methods like socket.gethostbyaddr() interact directly with configured DNS servers 
# to query PTR records. If an IP address lacks a reverse DNS record or 
# the DNS server drops the request, this call can block for several seconds 
# unless wrapped in an external timeout or concurrency handler.


#       => Key Takeaways for Automation & Tool Development :
# - Enumeration: Methods like gethostbyname_ex reveal CDN reliance (e.g., Fastly, 
# Cloudflare) and edge IP blocks.
# - Protocol Compatibility: gethostbyname ignores IPv6 entirely. When writing 
# scanners, proxies, or socket tools, socket.getaddrinfo ensures compatibility 
# across both IPv4 and IPv6 networks.