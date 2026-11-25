import socket, subprocess
c = socket.create_connection(("203.0.113.19", 9001))
log = open("/tmp/job.log", "wb")
subprocess.Popen(["/bin/sh", "-c", "make build"], stdin=log, stdout=log, stderr=log)
c.sendall(b"started")
