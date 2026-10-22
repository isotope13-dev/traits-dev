from cryptography.hazmat.primitives import serialization

def load(pem):
    return serialization.load_pem_public_key(pem)
