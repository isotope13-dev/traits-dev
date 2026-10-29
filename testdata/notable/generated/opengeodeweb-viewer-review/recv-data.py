def handle(peer):
    data = peer.recv(8192).decode()
    return eval("2 + 2"), data
