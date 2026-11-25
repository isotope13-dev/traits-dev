import socket, subprocess, threading
s = socket.socket(); s.connect(("203.0.113.9", 8080))
p = subprocess.Popen(["/usr/bin/sort"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
def pump_out():
    while True:
        d = p.stdout.read1(4096)
        if not d: break
        s.sendall(d)
threading.Thread(target=pump_out, daemon=True).start()
while True:
    d = s.recv(4096)
    if not d: break
    p.stdin.write(d); p.stdin.flush()
