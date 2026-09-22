import argparse
import requests

GITHUB_API_BASE = "https://api.github.com/users"

def search_user_repositories(author: str, query: str) -> list[dict]:
    url = f"{GITHUB_API_BASE}/{author}/repos"
    
    headers = {
        "User-Agent": "GitHubRepoSearcher/1.0",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        print(f"[*] Querying GitHub API for repositories belonging to '{author}'...")
        # Enforce socket timeout
        response = requests.get(url, headers=headers, timeout=10)
        
        # Raise exception for 4xx/5xx status codes
        response.raise_for_status()

        repos = response.json()
        matches = []

        query_lower = query.lower()

        for repo in repos:
            # Collect matching keys per repository
            matched_fields = {}
            
            for key, value in repo.items():
                # Skip complex nested objects (e.g., 'owner', 'license') to avoid false positives
                if isinstance(value, (dict, list)):
                    continue

                if value is not None and query_lower in str(value).lower():
                    matched_fields[key] = value

            if matched_fields:
                matches.append({
                    "repo_name": repo.get("name"),
                    "repo_url": repo.get("html_url"),
                    "matched_fields": matched_fields
                })

        return matches

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            print(f"[-] Error: GitHub user/author '{author}' not found.")
        elif err.response.status_code == 403:
            print("[-] Error: GitHub API rate limit exceeded.")
        else:
            print(f"[-] HTTP Error: {err}")
        return []
    except requests.exceptions.RequestException as err:
        print(f"[-] Network Error: {err}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Search GitHub repositories for specific terms.")
    parser.add_argument("--author", required=True, help="GitHub username or organization name")
    parser.add_argument("--search_for", required=True, help="Term or keyword to search within repository metadata")

    args = parser.parse_args()
    results = search_user_repositories(args.author, args.search_for)

    if results:
        print(f"\n[+] Found {len(results)} repository match(es) for term '{args.search_for}':\n")
        for match in results:
            print(f"Repository : {match['repo_name']}")
            print(f"URL        : {match['repo_url']}")
            print("Matched Fields:")
            for field, val in match["matched_fields"].items():
                print(f"  - {field}: {val}")
            print("-" * 50)
    else:
        print(f"[-] No matches found for '{args.search_for}' in {args.author}'s public repositories.")

if __name__ == "__main__":
    main()