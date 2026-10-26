"""Doctest-driven cipher tutorial: defining decrypt as the worked classroom
exercise is pedagogy, not dropper staging."""


def decrypt(word: str, key: int) -> str:
    """Shift each letter back by key positions.

    >>> decrypt("khoor", 3)
    'hello'
    """
    out = []
    for ch in word:
        if ch.isalpha():
            base = ord("a") if ch.islower() else ord("A")
            out.append(chr((ord(ch) - base - key) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)
