import ast
import base64
import marshal
import zlib

def wrap(source):
    data = base64.b64encode(marshal.dumps(compile(source, '<generated>', 'exec')))
    return f"import marshal, base64\nexec(marshal.loads(base64.b64decode({data!r})))\n"

def check(source):
    ast.parse(wrap(source))
