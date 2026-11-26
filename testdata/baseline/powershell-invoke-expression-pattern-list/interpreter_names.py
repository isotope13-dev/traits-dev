import re

_INTERPRETER = (
    r"(?:sh|bash|zsh|pwsh|powershell|iex|invoke-expression)(?:\.exe)?"
)

def interpreter_pattern():
    return re.compile(_INTERPRETER, re.IGNORECASE)
