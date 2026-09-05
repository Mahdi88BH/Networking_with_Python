#!/usr/bin/env python
# Shebang line: Tells the Unix/Linux OS to execute this file using 
# the environment's Python interpreter.
import os
import sys
from subprocess import Popen, PIPE


print("Operating system:",sys.platform)

if sys.platform.startswith("linux"):
    command_ping ='/bin/ping'
elif sys.platform == "darwin":
    command_ping ='/sbin/ping'
elif os.name == "nt":
    command_ping ='ping'

for ip in range(1,4):
    ipAddress = '192.168.1.'+str(ip)
    print("Scanning %s " %(ipAddress))

    # Launch the ping command process in the background.
    process = Popen(
        [command_ping, '-c 1',ipAddress], 
        stdin=PIPE, 
        stdout=PIPE, 
        stderr=PIPE)

    # communicate() sends data to stdin (None here) and waits for 
    # process completion.
    # It returns a tuple of byte strings: (stdout_data, stderr_data).
    stdout, stderr= process.communicate(input=None)

    print("stdout_data => ", stdout)
    if b"bytes from " in stdout:
        print("The Ip Address %s has responded with a ECHO_REPLY!" 
                %(stdout.split()[1]))