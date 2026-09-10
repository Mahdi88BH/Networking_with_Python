import ssl


# def main():

#     # DEPRECATION BUG: ssl.PROTOCOL_SSLv23 is deprecated since Python 3.6 and removed in newer 
#     # Python releases.
#     # While it historically meant "negotiate highest supported protocol", referencing SSLv23 
#     # is insecure practice.
#     ciphers = ssl.SSLContext(ssl.PROTOCOL_SSLv23).get_ciphers()

#     # Iterate over the array of cipher dictionaries returned by OpenSSL
#     for cipher in ciphers:
#         # Prints each cipher name (e.g. TLS_AES_256_GCM_SHA384) and its supported TLS/SSL protocol 
#         # string
#         print(f"{cipher['name']} => {cipher['protocol']}")



def main():
    # Recommended approach: create a default client context with modern security settings
    context = ssl.create_default_context()

    # Get list of active/enabled cipher suites configured for this context
    ciphers = context.get_ciphers()

    print(f"[*] Total Supported Ciphers Enabled: {len(ciphers)}\n")
    print(f"{'Cipher Name':<40} | {'Protocol':<10} | {'Secret Bits':<11} | {'Description'}")
    print("-" * 90)

    for cipher in ciphers:
        name = cipher.get('name', 'N/A')
        protocol = cipher.get('protocol', 'N/A')
        bits = cipher.get('alg_bits', 'N/A')
        description = cipher.get('description', '')

        print(f"{name:<40} | {protocol:<10} | {bits:<11} | {description[:25]}...")


if __name__ == "__main__":
    main()



# Key Issues & Modern Deprecations
# ssl.PROTOCOL_SSLv23 Deprecation:
# PROTOCOL_SSLv23 was named after legacy SSL versions. In Python 3.6+, it was deprecated in favor 
# of ssl.PROTOCOL_TLS (and ssl.PROTOCOL_TLS_CLIENT / ssl.PROTOCOL_TLS_SERVER in Python 3.10+).

# Default Context Best Practices (ssl.create_default_context()):
# Initializing ssl.SSLContext() directly without parameters creates an unconfigured context. 
# Using ssl.create_default_context() sets secure modern defaults (enforces certificate verification, 
# disables weak ciphers like SSLv2/SSLv3, and sets up system root CAs).