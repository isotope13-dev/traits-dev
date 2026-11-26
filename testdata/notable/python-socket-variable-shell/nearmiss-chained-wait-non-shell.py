import socket, subprocess
def main():
    s = socket.socket()
    s.connect(('198.51.100.4', 9001))
    subprocess.Popen(['/usr/bin/sort'], stdin=s, stdout=s, stderr=s).wait()
main()
