import ssl

left = bytearray(b"\x11\x22\x33")
key = b"\x42"
for i in range(len(left)):
    left[i] ^= key[i % len(key)]
right = bytes(value ^ key[i%len(key)] for value in left)

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
