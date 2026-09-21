import urllib.request
import urllib.error

def download_gzip_file(url: str, output_filename: str):
    # Set explicit User-Agent to avoid mirror blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        print(f"[*] Connecting to Debian mirror:\n    {url}")
        # Enforce a 15-second socket connection timeout
        with urllib.request.urlopen(req, timeout=15) as response:
            print(f"[+] Connected! Status: {response.status} {response.reason}")
            
            # Read total file size header if provided by server
            content_length = response.getheader('Content-Length')
            if content_length:
                print(f"[+] Total File Size: {int(content_length) / (1024 * 1024):.2f} MB")

            print(f"[*] Streaming payload to '{output_filename}' in 64KB chunks...")
            
            # Stream directly to disk using memory-safe chunking
            with open(output_filename, 'wb') as out_file:
                chunk_size = 64 * 1024  # 64KB buffer
                bytes_downloaded = 0
                
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break  # EOF reached
                    out_file.write(chunk)
                    bytes_downloaded += len(chunk)

            print(f"[+] Download complete! Saved {bytes_downloaded / (1024 * 1024):.2f} MB to disk.")

    except urllib.error.HTTPError as err:
        print(f"[-] HTTP Error {err.code}: {err.reason}")
    except urllib.error.URLError as err:
        print(f"[-] Network Error: {err.reason}")
    except KeyboardInterrupt:
        print("\n[-] Download canceled by user.")

if __name__ == "__main__":
    target_url = 'http://ftp.debian.org/debian/dists/stable/contrib/Contents-all.gz'
    download_gzip_file(target_url, 'Contents-all.gz')



# Critical Operational Risks
# 1. Out-of-Memory (OOM) Exhaustion
# Calling .read() directly on urlopen() forces Python to download the entire remote file into system RAM as a single byte array before saving it.

# While Contents-all.gz is around 20–30 MB, downloading multi-gigabyte files (like ISOs or database dumps) using this pattern will cause your script or 
# server to crash with a MemoryError.

# Fix: Use a while loop to stream chunks (e.g., 64KB at a time) directly from the network socket buffer onto disk.

# 2. Missing Context Managers (with blocks)
# If an exception occurs between open('Contents-all.gz', 'wb') and file.close(), the file descriptor remains open in operating system memory. 
# Using with open(...) as f: guarantees clean cleanup upon exit or failure.

# 3. Default User-Agent & Timeout Missing
# Debian FTP/HTTP mirrors may throttle or block default Python user-agent strings (Python-urllib/3.x). Additionally, omitting a timeout parameter means a 
# stalled connection will cause your script to hang indefinitely.