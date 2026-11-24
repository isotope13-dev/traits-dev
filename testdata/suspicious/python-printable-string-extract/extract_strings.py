import sys

def extract_printable(data):
    out = []
    cur = bytearray()
    for b in data:
        if 32 <= b < 127:
            cur.append(b)
        else:
            if len(cur) >= 4:
                out.append(cur.decode('ascii'))
            cur = bytearray()
    if len(cur) >= 4:
        out.append(cur.decode('ascii'))
    return out

if __name__ == '__main__':
    for s in extract_printable(open(sys.argv[1], 'rb').read()):
        print(s)
