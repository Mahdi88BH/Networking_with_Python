#!/usr/bin/python3
import os
from subprocess import call

print("Current path",os.getcwd())
print("PATH Environment variable:",os.getenv("PATH"))
print("List files using the subprocess module:")
# call(["ls", "-la"]) executes the system command 'ls -la' to list 
# all files and 
# permissions in long format. Output is printed directly to stdout 
# (terminal screen).
call(["ls", "-la"])

# subprocess.run() provides cleaner error checking (check=True), 
# timeout management, and easy output capturing (capture_output=True).