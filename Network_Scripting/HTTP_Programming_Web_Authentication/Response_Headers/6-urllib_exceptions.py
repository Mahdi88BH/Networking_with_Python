import urllib.error
from urllib.request import Request, urlopen

url = 'https://www.ietf.org/rfc/rfc0.txt'

def fetch_document(target_url):
    # Add a custom User-Agent to avoid generic request blocks
    req = Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        print(f"[*] Querying: {target_url} ...")
        # Enforce a 5-second socket timeout
        with urlopen(req, timeout=5) as response:
            print(f"[+] Success! Status: {response.status}")
            data = response.read().decode('utf-8')
            print(f"[+] Read {len(data)} characters.")

    # 1. Catch HTTP-specific response errors (404, 403, 500, etc.)
    except urllib.error.HTTPError as err:
        print(f"[-] HTTP Error Caught:")
        print(f"    Code:   {err.code}")
        print(f"    Reason: {err.reason}")
        print(f"    URL:    {err.url}")
        
        # You can inspect the server's raw error response payload:
        error_body = err.read().decode('utf-8', errors='ignore')
        print(f"    Server Error Payload Snippet: {error_body[:100]}...")

    # 2. Catch low-level network errors (DNS failure, connection refused, timeout)
    except urllib.error.URLError as err:
        print(f"[-] Network Level Failure:")
        print(f"    Reason: {err.reason}")

    # 3. Catch socket timeout errors explicitly if needed
    except TimeoutError:
        print("[-] Connection timed out before server responded.")

if __name__ == "__main__":
    fetch_document(url)