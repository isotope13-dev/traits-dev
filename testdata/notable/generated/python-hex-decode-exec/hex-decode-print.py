"""Show a hex-encoded greeting.

The message is stored as hex so that the sample table below stays aligned in
plain text. Decoding only produces a string for display; it is never handed to
an evaluator.
"""

SAMPLES = {
    "english": "68656c6c6f20776f726c64",
    "short": "6869",
}


def greeting(hex_text):
    """Decode hex text into a readable message."""
    return bytes.fromhex(hex_text).decode()


def style(text):
    """Wrap text in ANSI bold, using two-byte escapes only."""
    return "\x1b[1m" + text + "\x1b[0m"


for name, hex_text in SAMPLES.items():
    print(name, style(greeting(hex_text)))
