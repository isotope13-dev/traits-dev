import os, select, socket
peer = socket.create_connection(("203.0.113.9", 8080))
log = open("/tmp/relay.log", "ab")
while True:
    ready, _, _ = select.select([peer], [], [], 60)
    for s in ready:
        buf = s.recv(4096)
        if not buf:
            raise SystemExit
        log.write(buf); log.flush()
