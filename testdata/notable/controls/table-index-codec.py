alphabet = "amber birch cedar dawn".split()
encoded = "birch dawn".split()
payload = bytes(alphabet.index(token) % 256 for token in encoded)
print(payload)
