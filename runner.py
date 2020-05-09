import subprocess
import time
import os

subprocess.Popen("socat -d -d pty,raw,echo=0 pty,raw,echo=0", shell=True)
time.sleep(0.05)
socket_number = input("Enter first socket: /dev/pts/")
subprocess.Popen("python3 host-application.py " + socket_number, shell=True)
print("Host application started!")
socket_number = input("Enter second socket: /dev/pts/")
subprocess.Popen("python3 evb-mock.py " + socket_number, shell=True)
