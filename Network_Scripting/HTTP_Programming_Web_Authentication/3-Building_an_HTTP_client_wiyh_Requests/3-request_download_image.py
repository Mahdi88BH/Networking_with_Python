import shutil
import requests

def download_file_stream(url: str, output_path: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }

    try:
        print(f"[*] Connecting to {url} ...")
        # # stream=True prevents loading the entire payload into RAM immediately,
        # leaving the raw socket stream unread.
        # Enforce 10-second timeout and enable streaming
        with requests.get(url, headers=headers, stream=True, timeout=10) as response:
            # Raise HTTPError for 4xx/5xx responses before creating the file
            response.raise_for_status()

            # Ensure response.raw decodes Content-Encoding (gzip/deflate) automatically
            response.raw.decode_content = True

            print(f"[*] Streaming payload to '{output_path}' ...")
            # # 3. Open local output file in binary write mode ('wb')
            with open(output_path, 'wb') as out_file:
                # Use shutil.copyfileobj to stream directly from response.raw to out_file
                # response.raw provides the underlying file-like urllib3 response stream object.
                shutil.copyfileobj(response.raw, out_file)

            print(f"[+] Download successfully completed!")

    except requests.exceptions.HTTPError as err:
        print(f"[-] HTTP Error {err.response.status_code}: {err}")
    except requests.exceptions.RequestException as err:
        print(f"[-] Download failed: {err}")

if __name__ == "__main__":
    target_url = 'https://www.python.org/static/img/python-logo.png'
    download_file_stream(target_url, 'python_logo.png')