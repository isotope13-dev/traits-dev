import socket, subprocess
s = socket.create_connection(("metrics.internal", 2003))
out = subprocess.run("uptime", shell=True, capture_output=True).stdout
s.sendall(b"host.uptime " + out)
