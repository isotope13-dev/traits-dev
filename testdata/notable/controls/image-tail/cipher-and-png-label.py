from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decrypt_record(key, iv, record):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decoder = cipher.decryptor()
    return decoder.update(record) + decoder.finalize()

image_label = b'IEND\xae\x42\x60\x82'
