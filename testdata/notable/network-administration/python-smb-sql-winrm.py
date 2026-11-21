from impacket.smbconnection import SMBConnection
import pymssql
import winrm
def check(host, user, password):
    client = SMBConnection(host, host)
    client.login(user, password)
    print(client.listShares())
    database = pymssql.connect(server=host, user=user, password=password)
    remote = winrm.Session(host, auth=(user, password))
