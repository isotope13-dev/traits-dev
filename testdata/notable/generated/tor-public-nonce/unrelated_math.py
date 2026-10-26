def calculate(buffer, modulus):
    left = buffer[:32]
    right = buffer[32:]
    x = int.from_bytes(left, "little")
    y = int.from_bytes(right, "little")
    return ((x - y) * pow(y, -1, modulus)) % modulus
