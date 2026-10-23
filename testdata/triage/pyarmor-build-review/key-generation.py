from cryptography.fernet import Fernet

def create_key():
    return Fernet.generate_key()
