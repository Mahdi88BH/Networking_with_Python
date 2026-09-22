import json
import requests

def inspect_httpbin():
    target_url = "http://httpbin.org/get"

    try:
        print(f"[*] Querying endpoint: {target_url} ...")
        # Issue GET request with a 5-second socket timeout
        response = requests.get(target_url, timeout=5)

        print(f"[+] HTTP Status Code: {response.status_code} {response.reason}")

        if response.status_code == 200:
            # Parse JSON payload into Python dictionary
            payload = response.json()

            print("\n=== TOP-LEVEL JSON KEYS RETURNED BY SERVER ===")
            for key, val in payload.items():
                print(f"  {key}: {val}")

            print("\n=== CLIENT REQUEST HEADERS SENT ===")
            for header, value in response.request.headers.items():
                print(f"  {header}: {value}")

            print("\n=== SERVER RESPONSE HEADERS RECEIVED ===")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")

            # Safely fetch 'Server' header using .get() to prevent KeyError
            server_software = response.headers.get('Server', 'Header Not Provided')
            print(f"\n[+] Identified Server Software: {server_software}")

        else:
            print(f"[-] Request returned non-200 HTTP status code: {response.status_code}")

    except requests.exceptions.Timeout:
        print("[-] Error: Connection timed out before server responded.")
    except requests.exceptions.ConnectionError:
        print("[-] Error: Network failure or host unreachable.")
    except json.JSONDecodeError:
        print("[-] Error: Server response was not valid JSON.")
    except requests.exceptions.RequestException as err:
        print(f"[-] HTTP Error encountered: {err}")

if __name__ == "__main__":
    inspect_httpbin()