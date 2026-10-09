from hashlib import sha512
from nacl.signing import SigningKey

def sign(seed, message):
    return SigningKey(seed).sign(message).signature

def tor_prefix(secret):
    return sha512(b"Derive temporary signing key hash input" + secret).digest()[:32]
