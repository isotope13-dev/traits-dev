import socket, subprocess
def fetch():
    s = socket.socket()
    s.connect(('198.51.100.4', 9001))
    s.sendall(b'ping')
    log = open('/tmp/out.log', 'w')
    subprocess.Popen(['/bin/sh', '-c', 'date'], stdin=None, stdout=log, stderr=log).wait()
fetch()
