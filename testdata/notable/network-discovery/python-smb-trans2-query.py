from impacket.smbconnection import SMBConnection
from struct import pack

# Behavioral reconstruction of ordinary SMB share inventory.
# This is not recovered attacker source. It logs on, lists shares, and
# issues one benign transaction query without any pipe probe or probe
# status check.
TRANS2_QUERY_PATH_INFORMATION = 0x05


def inventory(target, user, password):
    client = SMBConnection(target, target)
    client.login(user, password)
    print(client.listShares())
    query = pack('<H', TRANS2_QUERY_PATH_INFORMATION)
    client.getSMBServer().send_trans(query)
    client.logoff()
