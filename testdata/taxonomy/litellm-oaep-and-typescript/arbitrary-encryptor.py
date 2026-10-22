from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def unrelated(pem, data, public_key):
    unused_key = serialization.load_pem_public_key(pem)
    return public_key.encrypt(data, padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
