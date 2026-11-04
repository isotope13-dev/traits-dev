from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
new_key = rsa.generate_private_key(public_exponent=3, key_size=3072)
encoded = new_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
certificate = x509.CertificateBuilder().sign(new_key, hashes.SHA384())
