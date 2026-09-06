import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time

url_list = [
    "http://www.python.org", 
    "http://www.google.com",
    "http://www.packtpub.com", 
    "http://www.goooooooogle.com"
    ]


def request_url(url):
    try:
        # 'stream=True' downloads only HTTP response headers immediately rather than reading full body content into RAM.
        response = requests.get(url, stream=True, timeout=3)
        return url + "-->" + str(response.status_code)
    except requests.exceptions.RequestException as e:
        # Return structured error message instead of letting thread crash
        return f"{url} --> FAILED ({type(e).__name__})"




def main():
    # Instantiate ThreadPoolExecutor capped at 10 concurrent worker threads.
    # 'with' context manager ensures all threads complete before execution proceeds past the block.
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(request_url, url) for url in url_list]


    # as_completed(futures) yields Future objects as soon as their underlying HTTP call completes.
    for task in as_completed(futures):
        # task.result() retrieves the return value of request_url(url).
        # NOTE: If request_url raised an exception (like requests.exceptions.ConnectionError), 
        #   task.result() re-raises it here!
        print(task.result())


if __name__ == '__main__':
    main()