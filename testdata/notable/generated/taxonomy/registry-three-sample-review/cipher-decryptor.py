from cryptography.hazmat.primitives.ciphers import Cipher
ctx = Cipher(algorithm, mode).decryptor()
