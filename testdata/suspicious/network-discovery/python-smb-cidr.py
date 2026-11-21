import ipaddress
import socket
import sys
from impacket.smbconnection import SMBConnection
import pymssql
import winrm

# Behavioral reconstruction of reported network and service discovery.
# This is not recovered attacker source. Credentials come from the operator.
def survey(user, password):
    network = ipaddress.ip_network('10.23.0.0/24')
    for address in network.hosts():
        host = str(address)
        for port in (445, 1433, 5985):
            with socket.socket() as probe:
                probe.settimeout(0.5)
                if probe.connect_ex((host, port)) != 0:
                    continue
            if port == 445:
                client = SMBConnection(host, host)
                client.login(user, password)
                print(client.listShares())
                client.logoff()
            elif port == 1433:
                database = pymssql.connect(server=host, user=user, password=password)
                database.close()
            else:
                remote = winrm.Session(host, auth=(user, password))
                print(remote)

if __name__ == '__main__':
    survey(sys.argv[1], sys.argv[2])
