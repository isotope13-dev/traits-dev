import socket
import ssl

EXECUTABLE = "pythonw.exe"
RESOURCE = "/messages"

def configured_reader(host: str = "127.0.0.1"):
    return socket.create_connection((host, 3011))

def lookup(obj, name):
    return obj.__getattribute__(name)

def accept_peer(listener):
    return listener.accept()

def private_ca_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_REQUIRED
    return ctx

CHROME = 'google-chrome --version'
