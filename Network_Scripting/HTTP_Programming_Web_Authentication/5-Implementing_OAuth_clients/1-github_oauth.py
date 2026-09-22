import json
import os
import sys
from requests_oauthlib import OAuth2Session

TOKEN_FILE = ".github_token.json"
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'

# Define explicit scopes needed for your script
SCOPES = ["read:user", "user:email", "repo"]

def get_credentials():
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    client_secret = os.environ.get("GITHUB_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("[-] Error: GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET environment variables must be set.")
        print("    Example: export GITHUB_CLIENT_ID='your_id'")
        print("             export GITHUB_CLIENT_SECRET='your_secret'")
        sys.exit(1)

    return client_id, client_secret

def save_token(token: dict):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token, f, indent=2)
    os.chmod(TOKEN_FILE, 0o600)  # Restrict permissions on Unix systems
    print(f"[+] Token saved securely to '{TOKEN_FILE}'.")

def load_token() -> dict | None:
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def authenticate_github(client_id: str, client_secret: str) -> OAuth2Session:
    token = load_token()

    if token:
        print("[*] Reusing saved access token ...")
        return OAuth2Session(client_id, token=token)

    print("[*] No saved token found. Initiating OAuth 2.0 Authorization Flow ...")
    github = OAuth2Session(client_id, scope=SCOPES)
    
    authorization_url, state = github.authorization_url(AUTHORIZATION_BASE_URL)
    print(f"\n[*] Open this link in your browser to authorize access:\n{authorization_url}\n")

    redirect_response = input("[*] Paste the full callback redirect URL here: ").strip()

    try:
        fetched_token = github.fetch_token(
            TOKEN_URL,
            client_secret=client_secret,
            authorization_response=redirect_response,
            headers={"Accept": "application/json"}
        )
        save_token(fetched_token)
        return github
    except Exception as err:
        print(f"[-] OAuth Token exchange failed: {err}")
        sys.exit(1)

def main():
    client_id, client_secret = get_credentials()
    github = authenticate_github(client_id, client_secret)

    print("\n[*] Querying GitHub API (/user) ...")
    try:
        response = github.get('https://api.github.com/user', timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"\n[+] Authenticated as: {user_data.get('login')} ({user_data.get('name')})")
            print(f"    Private Repos:     {user_data.get('total_private_repos', 'N/A')}")
            print(f"    Public Repos:      {user_data.get('public_repos')}")
            print(f"    Email:             {user_data.get('email', 'N/A')}")
        else:
            print(f"[-] API request failed: HTTP {response.status_code} - {response.text}")
            
    except Exception as err:
        print(f"[-] Network Error: {err}")

if __name__ == "__main__":
    main()


# The GitHub OAuth Authorization Code Flow :


# [ Your Script ]               [ User Browser ]              [ GitHub Auth Server ]         [ GitHub API ]
#        |                             |                                |                            |
#  1. Generate URL ------------------->|                                |                            |
#        |                             | --- 2. Visit Auth URL -------> |                            |
#        |                             | <-- 3. Grants Permission ----- |                            |
#        | <--- 4. Paste Callback URL -| (Contains authorization code)  |                            |
#        |                             |                                |                            |
#        | ------------------ 5. POST /access_token ------------------> |                            |
#        | <----------------- 6. Returns Access Token ----------------- |                            |
#        |                                                                                           |
#        | ------------------ 7. GET /user (with Bearer Token) ------------------------------------> |
#        | <----------------- 8. Returns JSON Profile Data ----------------------------------------- |