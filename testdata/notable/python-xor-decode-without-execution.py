payload = "hidden"
key = "123"
decoded = ""
for index, char in enumerate(payload):
    decoded += chr(ord(char) ^ ord(key[index % len(key)]))
print(decoded)
