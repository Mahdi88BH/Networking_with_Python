import argparse
from urllib.parse import urlparse, urljoin
import requests

DEFAULT_USER_AGENT = "SecurityScanner/1.0 (RobotsTxtInspector)"

def fetch_robots_txt(target_url: str):
    # Ensure scheme is present (http:// or https://)
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    # Normalize base URL using urllib.parse
    parsed = urlparse(target_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = urljoin(base_url, "/robots.txt")

    headers = {"User-Agent": DEFAULT_USER_AGENT}

    try:
        print(f"[*] Fetching: {robots_url} ...\n")
        # Set 5-second socket timeout
        response = requests.get(robots_url, headers=headers, timeout=5)

        if response.status_code == 200:
            print("=== ROBOTS.TXT CONTENT FOUND ===")
            print(response.text)
        elif response.status_code == 404:
            print("[-] robots.txt does not exist on this server (HTTP 404 Not Found).")
        else:
            print(f"[-] Unexpected HTTP status code: {response.status_code} {response.reason}")

    except requests.exceptions.Timeout:
        print("[-] Connection timed out while trying to reach the server.")
    except requests.exceptions.ConnectionError:
        print("[-] Failed to connect to host (DNS failure or connection refused).")
    except requests.exceptions.RequestException as err:
        print(f"[-] HTTP Request failed: {err}")

def main():
    # Clean CLI interface using built-in argparse module
    parser = argparse.ArgumentParser(description="Fetch and display robots.txt for a given domain.")
    parser.add_argument("url", help="Target URL or domain (e.g., example.com or https://example.com)")
    
    args = parser.parse_args()
    fetch_robots_txt(args.url)

if __name__ == "__main__":
    main()