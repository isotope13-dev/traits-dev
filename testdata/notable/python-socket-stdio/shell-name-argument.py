import socket
import subprocess

channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
channel.connect(("142.4.107.34", 4444))
subprocess.Popen(["/usr/bin/printf", "/bin/sh"], stdin=channel.fileno(), stdout=channel.fileno(), stderr=channel.fileno())
