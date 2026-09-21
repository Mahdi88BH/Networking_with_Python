import urllib.request
import urllib.error

url = 'http://ftp.debian.org/debian/dists/stable/contrib/Contents-all.gz'
output_filename = 'Contents-all.gz'

def download_file():
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)

    try:
        print(f"[*] Connecting to {url} ...")
        # Context manager closes HTTP socket connection automatically when done
        with urllib.request.urlopen(req, timeout=15) as file_gz, \
             open(output_filename, 'wb') as file:
            
            file_size = 0
            chunk_size = 64 * 1024  # 64KB buffer is more efficient for modern network cards

            # Stream chunks directly using the walrus operator
            while chunk := file_gz.read(chunk_size):
                file.write(chunk)
                file_size += len(chunk)

            print(f"[+] Download complete: {file_size:,} bytes copied to '{output_filename}'")

    except urllib.error.HTTPError as err:
        print(f"[-] HTTP Error {err.code}: {err.reason}")
    except urllib.error.URLError as err:
        print(f"[-] Network Error: {err.reason}")

if __name__ == "__main__":
    download_file()