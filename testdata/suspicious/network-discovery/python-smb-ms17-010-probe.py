from impacket import smb
from impacket.smbconnection import SMBConnection
from struct import pack

# Behavioral reconstruction of a published SMB probe pattern.
# This is not recovered attacker source. It checks one host for the
# MS17-010 named-pipe response without sending any exploit.
TRANS_PEEK_NMPIPE = 0x23


def probe(target):
    connection = SMBConnection(target, target)
    try:
        connection.login('', '')
    except smb.SessionError:
        return False
    finally:
        pass
    request = pack('<H', TRANS_PEEK_NMPIPE)
    reply = connection.getSMBServer().send_trans(request)
    status = reply.getNTStatus()
    if status == 0xC0000205:  # STATUS_INSUFF_SERVER_RESOURCES
        print('vulnerable: ' + target)
        return True
    return False
