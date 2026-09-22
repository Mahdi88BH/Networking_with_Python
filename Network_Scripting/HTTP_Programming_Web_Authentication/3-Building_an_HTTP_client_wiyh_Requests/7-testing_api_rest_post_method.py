import json
import requests

def send_json_post():
    target_url = "http://httpbin.org/post"
    payload = {"id": "0123456789"}

    try:
        print(f"[*] Sending JSON POST request to {target_url} ...")
        
        # 'json=' automatically handles JSON serialization AND sets 'Content-Type: application/json'
        # Add explicit timeout for production safety
        response = requests.post(target_url, json=payload, timeout=5)

        print(f"[+] HTTP Status Code: {response.status_code} {response.reason}")

        if response.status_code == 200:
            server_analysis = response.json()

            print("\n=== WHAT HTTPBIN RECEIVED FROM CLIENT ===")
            print(f"Parsed JSON Payload : {server_analysis.get('json')}")
            print(f"Form Data           : {server_analysis.get('form')}")
            print(f"Raw Body String     : {server_analysis.get('data')}")

            print("\n=== REQUEST HEADERS SENT ===")
            for header, value in response.request.headers.items():
                print(f"  {header}: {value}")

            print("\n=== RESPONSE HEADERS RECEIVED ===")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")

            # Safe lookup using .get()
            server_software = response.headers.get("Server", "Header Not Provided")
            print(f"\n[+] Server Software: {server_software}")

        else:
            print(f"[-] HTTP Request failed with status: {response.status_code}")

    except requests.exceptions.Timeout:
        print("[-] Connection timed out.")
    except requests.exceptions.RequestException as err:
        print(f"[-] Network Error: {err}")

if __name__ == "__main__":
    send_json_post()