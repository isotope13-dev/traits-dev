from hashlib import sha512
prefix = sha512(b"Derive temporary signing key hash input").digest()[:32]
