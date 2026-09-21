import urllib.request
import urllib.parse

# 1. Define dictionary containing form data key-value pairs
data_dictionary = {"id": "0123456789"}

# 2. URL-encode dictionary into application/x-www-form-urlencoded string ("id=0123456789")
data = urllib.parse.urlencode(data_dictionary)

# 3. Convert ASCII string to raw byte payload required by urllib.request.urlopen()
data = data.encode('ascii')

if __name__ == "__main__":
    # 4. Perform HTTP request to httpbin.org/post.
    # CRITICAL DETAIL: Passing 'data' automatically converts the HTTP request method from GET to POST!
    with urllib.request.urlopen("http://httpbin.org/post", data) as response:
        # 5. Read response byte stream from socket buffer and decode UTF-8 string JSON payload
        print(response.read().decode('utf-8'))



# Modern Third-Party Alternative: requests
# In production Python security tooling, urllib is rarely used for HTTP tasks because of its verbose API. Most security tools use 
# the third-party requests library or httpx:

# import requests

# # Form-encoded POST request
# resp = requests.post("http://httpbin.org/post", data={"id": "0123456789"})

# # JSON-encoded POST request
# # resp = requests.post("http://httpbin.org/post", json={"id": "0123456789"})

# print(resp.json())