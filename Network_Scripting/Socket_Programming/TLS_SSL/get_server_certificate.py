import ssl
import socket
from pprint import pprint


# def main():

#     addr = ('python.org', 443)

#     # Retrieves the raw, PEM-encoded X.509 server certificate directly from the target socket address.
#     # NOTE: This convenience function fetches the raw certificate string, but it does NOT perform 
#     # certificate validation/chain verification!
#     certificate = ssl.get_server_certificate(addr)
#     print(certificate)


def main():
    hostname = 'python.org'
    port = 443

    # Create a secure context configured with default CA trust stores and validation rules
    context = ssl.create_default_context()

    # Establish TCP connection
    with socket.create_connection((hostname, port)) as sock:
        # Wrap the TCP socket with TLS layer
        with context.wrap_socket(sock, server_hostname=hostname) as tls_sock:
            # Retrieve the verified and parsed certificate dictionary
            cert = tls_sock.getpeercert()
            
            print(f"[*] Successfully retrieved certificate for {hostname}:\n")
            print(f"Subject: {cert.get('subject')}")
            print(f"Issuer:  {cert.get('issuer')}")
            print(f"Valid From: {cert.get('notBefore')}")
            print(f"Valid Until: {cert.get('notAfter')}\n")
            
            print("Full Parsed Certificate Dictionary:")
            pprint(cert)


if __name__ == "__main__":
    main()




# Key Operational Detail: ssl.get_server_certificate()
# 1. What it does
# ssl.get_server_certificate() is a low-level helper function provided by Python's ssl module. 
# It performs a basic TLS handshake with the specified server (python.org:443), retrieves 
# the public server certificate provided during the handshake, and returns 
# it as a PEM-formatted ASCII string.

# 2. The Major Limitation (No Chain Validation)
# By default in Python versions prior to 3.10, ssl.get_server_certificate() fetches the certificate 
# without validating whether it is signed by a trusted Certificate Authority (CA) or checking 
# for host name mismatches.

# If you want to extract detailed certificate metadata (such as the expiration date, issuer, 
# subject name, or SANs) securely, you should connect using an ssl.SSLContext configured with 
# full verification enabled.