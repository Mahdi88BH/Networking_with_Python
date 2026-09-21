import urllib.request
import urllib.error
import re

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def extract_emails_from_url(target_url: str):
    # Ensure URL includes scheme (http:// or https://)
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    # Construct request with custom User-Agent directly (avoiding global state mutation)
    req = urllib.request.Request(
        target_url, 
        headers={'User-Agent': USER_AGENT}
    )

    # Standard RFC 5322 compliant regex for extracting email addresses
    email_pattern = re.compile(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 
        re.IGNORECASE
    )

    try:
        print(f"[*] Fetching: {target_url} ...")
        with urllib.request.urlopen(req, timeout=10) as response:
            # Decode raw socket bytes to UTF-8 text string
            raw_bytes = response.read()
            html_text = raw_bytes.decode('utf-8', errors='ignore')

            # Extract all matches and deduplicate using a set
            found_emails = set(re.findall(email_pattern, html_text))

            if found_emails:
                print(f"[+] Found {len(found_emails)} unique email(s):")
                for email in sorted(found_emails):
                    print(f"  - {email}")
            else:
                print("[-] No email addresses found on the target page.")

    except urllib.error.HTTPError as err:
        print(f"[-] HTTP Error {err.code}: {err.reason}")
    except urllib.error.URLError as err:
        print(f"[-] Network Error: {err.reason}")
    except Exception as err:
        print(f"[-] Unexpected Error: {err}")

if __name__ == "__main__":
    user_input = input("Enter target URL: ").strip()
    if user_input:
        extract_emails_from_url(user_input)