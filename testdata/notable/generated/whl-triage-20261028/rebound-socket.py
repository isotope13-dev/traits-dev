import socket,subprocess

def launch(address,other):
    peer=socket.socket()
    peer.connect(address)
    peer=other
    subprocess.Popen(['python','widget.py'],stdin=peer,stdout=peer)
