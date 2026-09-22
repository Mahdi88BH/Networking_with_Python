import requests

def get_github_user(username: str):
    url = f"https://api.github.com/users/{username}"
    
    # Best Practice: Always supply a custom User-Agent header when querying GitHub APIs
    headers = {
        "User-Agent": "PythonSecurityScript/1.0",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        print(f"[*] Querying GitHub API for user/org: '{username}' ...")
        # Enforce a 5-second socket connection and read timeout
        response = requests.get(url, headers=headers, timeout=5)

        # Raise an exception for 4xx/5xx responses (e.g., 404 User Not Found)
        response.raise_for_status()

        # Parse JSON payload into a Python dictionary
        user_data = response.json()

        print(f"\n[+] User Found: {user_data.get('name', username)}")
        print(f"  - Profile URL:    {user_data.get('html_url')}")
        print(f"  - Location:       {user_data.get('location', 'N/A')}")
        print(f"  - Public Repos:   {user_data.get('public_repos')}")
        print(f"  - Followers:      {user_data.get('followers')}")

        # Inspect API Rate Limit Headers returned by GitHub
        rate_limit = response.headers.get('X-RateLimit-Remaining')
        print(f"\n[*] GitHub API Rate Limit Remaining: {rate_limit} requests this hour.")

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            print(f"[-] Error: GitHub user/org '{username}' not found.")
        else:
            print(f"[-] HTTP Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"[-] Network Error: {err}")

if __name__ == "__main__":
    get_github_user("ridamellouki3")