from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
public_key = load_pem_public_key(pem)
public_key.verify(signature, data, padding, hashes.SHA256())
