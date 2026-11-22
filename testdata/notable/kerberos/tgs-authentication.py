from impacket.krb5.kerberosv5 import getKerberosTGS

def authenticate(spn, realm, dc, tgt, cipher, key):
    return getKerberosTGS(spn, realm, dc, tgt, cipher, key)
