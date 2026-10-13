import socket
import ssl

EXECUTABLE = "python.exe"
RESOURCE = "/notifications"

def configured_reader(host: str = "192.0.2.1"):
    return socket.create_connection(("127.0.0.1", 3011))

def lookup(obj):
    return obj.name

def configure(listener):
    listener.listen(1)

def verified_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = True
    return ctx

CHROME = '/usr/bin/google-chrome'
