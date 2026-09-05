import subprocess
import sys
import os

print("Operating system:",sys.platform)

# Set the binary path for the ping command depending on the operating
#  system platform.
if sys.platform.startswith("linux"):
    command_ping ='/bin/ping'   # Standard Linux ping path
elif sys.platform == "darwin":
    command_ping = '/sbin/ping' # Standard macOS ping path
elif os.name == "nt":
    command_ping ='ping'        # Windows system ping executable

ping_parameter ='-c 1'
domain = "www.google.com"

# Start the ping command as a background subprocess using Popen.
# shell=False: Prevents shell injection vulnerabilities by passing 
# arguments securely as a list.
# stderr=subprocess.PIPE: Redirects stderr output so Python can read 
# error logs.
p = subprocess.Popen(
    [command_ping,ping_parameter,domain], 
    shell=False, 
    stderr=subprocess.PIPE
    )

# Read the first single byte (1 character) from the stderr 
# stream buffer.
out = p.stderr.read(1)

# Decode the captured raw byte into a UTF-8 string and write it 
# directly to the terminal stdout.
sys.stdout.write(str(out.decode('utf-8')))

# Force the stdout buffer to flush immediately so the printed 
# character appears in the terminal without waiting.
sys.stdout.flush()