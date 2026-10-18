def make_pdf(objects):
    output = bytearray(b"%PDF-1.4\n")
    for i, obj in enumerate(objects, 1):
        output += obj
    return output

def slice_copy(data, i):
    return bytes(data[i+1:])
