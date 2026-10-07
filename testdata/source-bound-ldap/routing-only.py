import socket
from impacket.ldap import ldap, ldapasn1

original_connect = socket.socket.connect

def routed_connect(self, destination):
    self.bind(("192.0.2.10", 0))
    return original_connect(self, destination)

socket.socket.connect = routed_connect

