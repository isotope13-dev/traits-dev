import os
import socket


def show():
    print(socket.gethostname(), len(os.environ))
