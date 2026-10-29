import requests
import hashlib
import os
from Crypto.Cipher import ARC4
from typing import Optional

KEY_LENGTH = 128  # must be below 256, above 1
SUM_LENGTH = 16   # MD5 length

def packet_make0501(data: bytes) -> bytes:
    # generate random key
    key = os.urandom(KEY_LENGTH)

    # create RC4 cipher
    cipher = ARC4.new(key)

    # encrypt the data
    encrypted_data = cipher.encrypt(data)

    # build packet
    packet = bytearray(SUM_LENGTH + KEY_LENGTH + len(data))
    packet[SUM_LENGTH:SUM_LENGTH+KEY_LENGTH] = key
    packet[SUM_LENGTH+KEY_LENGTH:] = encrypted_data

    # compute checksum
    checksum = hashlib.md5(packet[SUM_LENGTH:]).digest()
    packet[:SUM_LENGTH] = checksum

    return bytes(packet)

def packet_decode0501(data: bytes) -> Optional[bytes]:
    if len(data) < (SUM_LENGTH + KEY_LENGTH):
        return None

    # validate checksum
    checksum = hashlib.md5(data[SUM_LENGTH:]).digest()
    if checksum != data[:SUM_LENGTH]:
        return None

    key = data[SUM_LENGTH:SUM_LENGTH+KEY_LENGTH]
    encrypted_data = data[SUM_LENGTH+KEY_LENGTH:]

    cipher = ARC4.new(key)
    decrypted_data = cipher.decrypt(encrypted_data)

    return decrypted_data

def htxp_exchange0501(url: str, data: str) -> str:
    packet = packet_make0501(data.encode())

    try:
        resp = requests.post(url, data=packet, headers={'Content-Type': 'application/octet-stream'})
        resp.raise_for_status()
    except Exception as e:
        print("err", e)
        return "", e

    plain = packet_decode0501(resp.content)
    return plain.decode() if plain else "", None
