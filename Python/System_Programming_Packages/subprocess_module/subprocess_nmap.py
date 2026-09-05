from subprocess import Popen, PIPE

process = Popen(['nmap','192.168.1.1'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

print(stdout.decode())