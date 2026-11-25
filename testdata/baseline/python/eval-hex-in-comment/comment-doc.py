import re

# Example of an obfuscated payload, documented but never executed:
#   eval("\x63\x75\x72\x6c")
PATTERN = re.compile(r"\d+")


def first_number(text: str) -> str:
    match = PATTERN.search(text)
    return match.group(0) if match else ""
