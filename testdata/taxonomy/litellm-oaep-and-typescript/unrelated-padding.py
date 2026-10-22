from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def wrap_key(pem, session_key):
    public_key = serialization.load_pem_public_key(pem)
    unused = padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),
                          algorithm=hashes.SHA256(), label=None)
    return public_key.encrypt(session_key, padding.PKCS1v15())
