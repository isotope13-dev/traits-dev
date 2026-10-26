import frida
import requests
device = frida.get_usb_device()
session = device.attach("target")
script = session.create_script("send({nonce: 'challenge'})")
response = requests.post("https://example.invalid/attest", json={"nonce": "challenge"})
script.post({"response": response.json()})
