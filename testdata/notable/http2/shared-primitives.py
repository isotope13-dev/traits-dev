import ssl
PREFACE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
MAX = 0x7fffffff
def test_arithmetic(f, a, b):
    x = f(a, MAX - 1)
    y = f(b, MAX - 1)
    return x, y
def refresh(lib, handle):
    lib.SSL_key_update(handle, 1)








for i in range(262144):
    print(i)
