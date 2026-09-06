# This script uses concurrent.futures.ThreadPoolExecutor to manage a pool of worker threads, 
#   asynchronously submitting tasks to be processed by available threads.
from concurrent.futures import ThreadPoolExecutor
import threading



def task(n):
    print(f"Processing {n} on Thread ID :{threading.get_ident()} name as {threading.current_thread()}")


def main():
    print("Starting ThreadPoolExecutor.......")
    # Using 'with' automatically waits for ALL threads to complete before exiting the block
    with ThreadPoolExecutor(max_workers=3) as executor:
        items = [2, 3, 4]
        # executor.map applies 'task' to every element in 'items' concurrently
        executor.map(task, items)

    print("All Tasks Completed")


if __name__ == "__main__":
    main()

# Use a context manager (with ThreadPoolExecutor(...) as executor:). It automatically calls .shutdown(wait=True) 
#   at the exit block, ensuring all threads complete before execution continues past the block.






# ===============OLD Version=================

# # Function executed by worker threads in the pool.
# def task(n):
#     print("Processing {}".format(n))

#     # threading.get_ident() returns the unique OS/kernel Thread ID (integer) for the current thread.
#     print("Accessing thread : {}".format(threading.get_ident()))

#     # threading.current_thread() returns the Thread object, printing its default name (e.g., ThreadPoolExecutor-0_0).
#     print("Thread Executed {}".format(threading.current_thread()))

# def main():
#     print("Starting ThreadPoolExecutor")
#     # Initialize a thread pool manager restricted to a maximum of 3 concurrent worker threads.
#     executor = ThreadPoolExecutor(max_workers=3)
#     future = executor.submit(task, (2))
#     future = executor.submit(task, (3))
#     future = executor.submit(task, (4))
#     print("All tasks complete")


# if __name__ == '__main__':
#     main()