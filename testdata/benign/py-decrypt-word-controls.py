"""Library decrypt call without a local decrypt definition: mentioning (and
calling) decrypt is ordinary crypto use, not a staged decryption routine."""

from cryptography.fernet import Fernet


def load_secret(token: bytes, key: bytes) -> bytes:
    cipher = Fernet(key)
    # decrypt the stored token with the caller's key
    return cipher.decrypt(token)
