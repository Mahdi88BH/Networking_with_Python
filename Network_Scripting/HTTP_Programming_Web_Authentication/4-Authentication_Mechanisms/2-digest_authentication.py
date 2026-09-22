import requests
from requests.auth import HTTPDigestAuth
from getpass import getpass

def test_digest_auth():
    target_url = 'http://httpbin.org/digest-auth/auth/user/pass'
    
    username = input("Enter username [default: user]: ").strip() or "user"
    password = getpass("Enter password [default: pass]: ") or "pass"

    try:
        print(f"[*] Initiating Digest Auth against {target_url} ...")
        
        # Issue request with HTTPDigestAuth and a 5-second socket timeout
        response = requests.get(
            target_url, 
            auth=HTTPDigestAuth(username, password),
            timeout=5
        )

        # Inspect challenge history
        if response.history:
            challenge_response = response.history[0]
            print(f"[*] Server Challenge Received: HTTP {challenge_response.status_code}")
            print(f"    WWW-Authenticate Header: {challenge_response.headers.get('WWW-Authenticate')}")

        print(f"\n[+] Final Response Status: {response.status_code} {response.reason}")

        if response.status_code == 200:
            print("\n=== AUTHENTICATED REQUEST HEADERS SENT ===")
            print(f"Authorization: {response.request.headers.get('Authorization')}")

            print("\n=== SERVER RESPONSE PAYLOAD ===")
            payload = response.json()
            print(f"Authenticated User: {payload.get('user')}")
            print(f"Authentication Result: {payload.get('authenticated')}")

        elif response.status_code == 401:
            print("[-] Authentication Failed: Invalid username or password.")
        else:
            print(f"[-] Unexpected HTTP response: {response.status_code}")

    except requests.exceptions.Timeout:
        print("[-] Connection timed out.")
    except requests.exceptions.RequestException as err:
        print(f"[-] Network Error: {err}")

if __name__ == "__main__":
    test_digest_auth()


#       => What Happens Behind the Scenes: The Digest Handshake

# When you inspect response.request.headers['Authorization'], you will see something similar to this header generated automatically by requests:
# > Authorization: Digest username="user", realm="me@httpbin.org", nonce="a1b2c3d4...", uri="/digest-auth/auth/user/pass", response="f3e2d1...", 
# qop=auth, nc=00000001, cnonce="e5f6g7..."

# Here is how requests handles this multi-turn handshake:

# Client (requests)                   Server (httpbin)
#        |                                   |
#        | ------ 1. GET /digest-auth -----> | (Initial request, no auth)
#        | <----- 2. 401 Unauthorized ------ | (Contains WWW-Authenticate header + nonce)
#        |                                   |
# [Computes Hash:                            |
#  HA1 = MD5(user:realm:pass)                |
#  HA2 = MD5(GET:uri)                        |
#  Response = MD5(HA1:nonce:nc:cnonce:qop:HA2)]
#        |                                   |
#        | ------ 3. GET /digest-auth -----> | (With Authorization: Digest header)
#        | <----- 4. 200 OK ---------------- | (Access Granted!)