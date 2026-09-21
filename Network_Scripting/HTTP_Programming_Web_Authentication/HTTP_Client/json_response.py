import json
import urllib.request

# Target HTTP endpoint for testing GET requests
url = "http://httpbin.org/get"

if __name__ == "__main__":
    # 1. Open HTTP connection and receive response stream context manager
    with urllib.request.urlopen(url) as response_json:
        
        # 2. Read raw response bytes, decode UTF-8 string, and parse JSON into Python dict
        data_json = json.loads(response_json.read().decode('utf-8'))
        
        # 3. Print parsed dictionary
        print(data_json)


# Key Observations & Refinements
# 1. Direct Stream Parsing with json.load()
# Instead of chaining .read().decode('utf-8') and passing a string into json.loads(), Python's json module offers json.load() (without the 's').

# json.load() accepts a file-like byte stream directly, reading and decoding the stream on the fly:

# # Stream directly into the JSON parser:
# data_json = json.load(response_json)

# 2. Handling HTTP & Network Errors
# When writing security tools or web scripts with urllib, HTTP errors (like 404 Not Found or 500 Server Error) and network failures (like DNS resolution failure 
# or timeouts) raise specific exceptions.

# Wrapping requests with urllib.error.HTTPError and urllib.error.URLError prevents your program from crashing unexpectedly.

# Production-Grade Script with Error Handling
# Here is the robust version with status code verification, stream parsing, and error catching:

# import json
# import urllib.request
# import urllib.error

# url = "http://httpbin.org/get"

# def main():
#     # Set custom User-Agent to avoid being blocked by default Python headers
#     req = urllib.request.Request(
#         url, 
#         headers={"User-Agent": "PythonNetworkClient/1.0"}
#     )

#     try:
#         # Add explicit socket timeout (5 seconds) to avoid indefinite hangs
#         with urllib.request.urlopen(req, timeout=5) as response:
#             print(f"[*] HTTP Status Code: {response.status}")
            
#             # Parse response stream directly into a Python dictionary
#             data = json.load(response)
            
#             print("[*] Successfully parsed JSON response:\n")
#             print(f"Client IP:     {data.get('origin')}")
#             print(f"URL Requested: {data.get('url')}")
#             print(f"Headers Sent:  {json.dumps(data.get('headers'), indent=2)}")

#     except urllib.error.HTTPError as err:
#         print(f"[-] HTTP Error Encountered: {err.code} - {err.reason}")
#     except urllib.error.URLError as err:
#         print(f"[-] Network/URL Error Encountered: {err.reason}")
#     except json.JSONDecodeError:
#         print("[-] Failed to parse response as JSON.")

# if __name__ == "__main__":
#     main()