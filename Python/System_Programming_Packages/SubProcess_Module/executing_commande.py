import sys
import subprocess





if __name__ == "__main__":
    # Execute the 'ls -l' command to list files in long format.
    # stdout=subprocess.PIPE captures the command's stdout output 
    # instead of printing it directly to the terminal.
    process = subprocess.run(('ls', '-l'), stdout=subprocess.PIPE)
    # process.stdout returns raw bytes. `.decode('utf-8')` converts 
    # those raw bytes into a readable Python string before printing.
    print(process.stdout.decode('utf-8'))


    try:
        # check=True forces Python to raise a 'subprocess.CalledProcessError' 
        # exception if the command exits with a non-zero code.
        process = subprocess.run(
            ('find', '/folder_not_exist', '.'),
            stdout=subprocess.PIPE,
            check=True)
        print(process.stdout.decode('utf_8'))
    except subprocess.CalledProcessError as error:
        print('Error =>', error)

    # Execute a inline Python script using sys.executable that 
    # explicitly raises a ValueError.
    # Because check=True is set, this line will crash the execution 
    # here with a CalledProcessError
    result = subprocess.run(
        [sys.executable, "-c", "raise ValueError('error')"], 
        check=True)

    # Run a command that sleeps for 10 seconds, but enforce a 5-second 
    # timeout limit.
    # NOTE: This line will raise a 'subprocess.TimeoutExpired' exception 
    # because 10s > 5s.
    result = subprocess.run(
        [sys.executable, "-c", "import time; time. sleep(10)"], 
        timeout=5)

    # Execute an inline Python script that reads from standard input 
    # (sys.stdin).
    # 'input=b"python"' passes byte data directly into the subprocess's 
    # stdin stream.
    result = subprocess.run(
        [sys.executable, "-c", "import sys; print(sys.stdin.read())"],
    input=b"python")