import json
import requests

def inspect_url(raw_url: str):
    url = raw_url.strip()

    # Default to HTTPS if no protocol scheme is provided
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        print(f"[*] Connecting to {url} ...")
        # Enforce a 5-second connection & read timeout
        response = requests.get(
            url, 
            headers={"User-Agent": "PythonHeaderInspector/1.0"}, 
            timeout=5
        )

        print(f"\n[+] Status Code: {response.status_code} {response.reason}")
        print(f"[+] Final Resolved URL: {response.url}")

        print("\n=== REQUEST HEADERS SENT BY CLIENT ===")
        for key, val in response.request.headers.items():
            print(f"  {key}: {val}")

        print("\n=== RESPONSE HEADERS RECEIVED FROM SERVER ===")
        for key, val in response.headers.items():
            print(f"  {key}: {val}")

        # Safely attempt JSON parsing if Content-Type indicates JSON
        print("\n=== RESPONSE BODY ANALYSIS ===")
        content_type = response.headers.get("Content-Type", "")
        
        if "application/json" in content_type:
            try:
                json_data = response.json()
                print("[+] Valid JSON Payload Detected:\n")
                print(json.dumps(json_data, indent=2))
            except json.JSONDecodeError:
                print("[-] Server claimed JSON content-type but returned malformed payload.")
        else:
            print(f"[*] Non-JSON Content-Type ('{content_type}'). Body preview:")
            print(response.text[:300] + ("..." if len(response.text) > 300 else ""))

    except requests.exceptions.Timeout:
        print("[-] Connection timed out before server responded.")
    except requests.exceptions.ConnectionError:
        print("[-] Failed to connect (DNS failure, host unreachable, or connection refused).")
    except requests.exceptions.RequestException as err:
        print(f"[-] HTTP Error: {err}")

if __name__ == "__main__":
    user_input = input("Enter target URL: ")
    if user_input.strip():
        inspect_url(user_input)