import ast
import base64

def wrap(source):
    return f"exec({source!r})\n"

def transform(source):
    decoded = base64.b64decode(source)
    ast.parse(wrap(decoded))
    return decoded
