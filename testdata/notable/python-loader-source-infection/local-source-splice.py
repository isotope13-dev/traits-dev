import os, re
_RE = re.compile("# managed block")

def _anchor(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if line.strip() == "colorama.init()":
            return index + 1
    for index, line in enumerate(lines):
        if line.startswith("if __name__"):
            return index
    last = -1
    for index, line in enumerate(lines):
        if line.rstrip("\r\n").startswith(("import ", "from ")) and not line.startswith((" ", "\t")):
            last = index
    return last + 1 if last >= 0 else max(1, len(lines) // 2)

def _write(path: str, text: str) -> bool:
    backup = path + ".bak"
    temp = os.path.join(os.path.dirname(path), "." + os.path.basename(path) + ".hx")
    try:
        if not os.path.exists(backup):
            with open(path, "rb") as source, open(backup, "wb") as target:
                target.write(source.read())
        with open(temp, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        os.replace(temp, path)
        return True
    except Exception:
        try:
            os.remove(temp)
        except Exception:
            pass
        return False

def _place(path: str, block: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8", newline="") as handle:
            source = handle.read()
    except Exception:
        return False
    if _RE.search(source):
        return False
    lines = source.splitlines(keepends=True)
    at = _anchor(lines)
    nl = "\r\n" if "\r\n" in source else "\n"
    head = "".join(lines[:at]).rstrip("\r\n") + nl + nl
    tail = "".join(lines[at:]).lstrip("\r\n")
    return _write(path, head + block.rstrip("\r\n").replace("\n", nl) + nl + nl + tail)
