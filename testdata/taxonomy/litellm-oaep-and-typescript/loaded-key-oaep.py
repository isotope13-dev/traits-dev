from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def wrap_key(pem, session_key):
    recipient = serialization.load_pem_public_key(pem)
    return recipient.encrypt(session_key, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))
