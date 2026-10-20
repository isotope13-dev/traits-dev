import ast
import base64
import marshal
import zlib

def wrap(source):
    return f"exec({source!r})\n"

ast.parse(wrap('pass'))
exec(marshal.loads(zlib.decompress(base64.b64decode('eJwDAAAAAAE='))))
