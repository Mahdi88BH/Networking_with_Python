import urllib.request
import urllib.error

def download_file(url: str, output_filename: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        print(f"[*] Connecting to {url} ...")
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"[+] HTTP Status: {response.status} {response.reason}")
            
            # Extract Content-Length header if provided by server
            content_length = response.getheader('Content-Length')
            if content_length:
                print(f"[+] File Size: {int(content_length):,} bytes")

            # Open local file in binary write mode ('wb') and stream in chunks
            print(f"[*] Saving to '{output_filename}' ...")
            with open(output_filename, "wb") as out_file:
                chunk_size = 4096  # Read 4KB chunks
                bytes_downloaded = 0
                
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break  # End of file reached
                    out_file.write(chunk)
                    bytes_downloaded += len(chunk)

            print(f"[+] Successfully downloaded {bytes_downloaded:,} bytes.")

    except urllib.error.HTTPError as err:
        print(f"[-] HTTP Error: {err.code} {err.reason}")
    except urllib.error.URLError as err:
        print(f"[-] Network Error: {err.reason}")

if __name__ == "__main__":
    target_url = "https://www.python.org/static/img/python-logo.png"
    download_file(target_url, "python_logo.png")



# 2. Redundant Double Download (urlretrieve vs urlopen)
# urllib.request.urlretrieve(url, "python.png") is a legacy convenience function that downloads the file and saves it to disk in one shot. 
# By calling urlretrieve first and then calling urlopen immediately after, your script downloads the same image twice over the network, 
# wasting bandwidth and making redundant HTTP requests.