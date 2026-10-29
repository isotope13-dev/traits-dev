def dispatch(peer):
    command = peer.recv(8192).decode().strip()
    return eval(command)
