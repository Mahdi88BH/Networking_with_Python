import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass

def main():
    username = input("Enter GitHub username: ")
    # Enter your Personal Access Token (PAT) when prompted for password
    token = getpass("Enter Personal Access Token: ")

    response = requests.get(
        'https://api.github.com/user', 
        auth=HTTPBasicAuth(username, token)
    )

    print(f"Response status code: {response.status_code}")

    if response.status_code == 200:
        user_data = response.json()
        print(f"Login successful! Welcome, {user_data.get('name') or username}.")
    else:
        print(f"Authentication failed: {response.json().get('message')}")


if __name__ == "__main__":
    main()