import socket, subprocess
def run(host):
    s = socket.create_connection((host, 80))
    s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
    log = open("build.log", "w")
    subprocess.Popen(["/bin/sh", "build.sh"], stdout=log, stderr=log)
    return s.recv(256)
