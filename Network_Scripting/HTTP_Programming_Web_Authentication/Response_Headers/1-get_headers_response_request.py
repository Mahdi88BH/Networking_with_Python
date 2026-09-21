import urllib.request
from urllib.request import Request
import urllib.error

def fetch_with_custom_user_agent(url, user_agent):
    # Construct Request object with explicit headers
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    request = Request(url, headers=headers)

    print("=== CLIENT OUTGOING REQUEST HEADERS ===")
    for header, value in request.header_items():
        print(f"{header}: {value}")
    print("=" * 40 + "\n")

    try:
        # Execute the HTTP request passing the configured Request object
        with urllib.request.urlopen(request, timeout=5) as response:
            print(f"[*] HTTP Status Code: {response.status} {response.reason}")
            print("=== SERVER INCOMING RESPONSE HEADERS ===")
            for header, value in response.getheaders():
                print(f"{header}: {value}")
                
    except urllib.error.HTTPError as err:
        print(f"[-] HTTP Error: {err.code} {err.reason}")
    except urllib.error.URLError as err:
        print(f"[-] Network Error: {err.reason}")

if __name__ == "__main__":
    target_url = "http://python.org"
    mobile_user_agent = (
        'Mozilla/5.0 (Linux; Android 10) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/83.0.4103.101 Mobile Safari/537.36'
    )

    fetch_with_custom_user_agent(target_url, mobile_user_agent)