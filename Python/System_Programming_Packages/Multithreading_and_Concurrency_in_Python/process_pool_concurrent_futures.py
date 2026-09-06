# This script uses concurrent.futures.ProcessPoolExecutor to distribute work across separate operating system processes, 
#   bypassing Python's Global Interpreter Lock (GIL) and leveraging multiple CPU cores.
import os
# Import ProcessPoolExecutor to manage a pool of separate OS processes.
from concurrent.futures import ProcessPoolExecutor


# Task function executed inside child processes.
def task():
    # os.getpid() retrieves the unique Process ID assigned by the OS.
    # Each worker in a ProcessPoolExecutor has a distinct PID from the main process.
    print(f"Executing our Task on Process {os.getpid()}")


def main():

    # Using 'with' guarantees process shutdown and output flushing
    with ProcessPoolExecutor(max_workers=3) as executor:
        # Asynchronously submit tasks to the process pool.
        # Each call returns a Future object instantly without blocking the main script.
        task1 = executor.submit(task)
        task2 = executor.submit(task)
    

if __name__ == '__main__':
    main()

# Because the script does not use a with context manager (or call executor.shutdown(wait=True)), 
#   the main process may finish executing main() and exit before the child worker processes finish initializing, 
#   running task(), and printing to stdout.