import subprocess


def load(source, target, key):
    with open(source, "rb") as f1, open(target, "wb") as f2:
        while True:
            byte = f1.read(1)
            if not byte:
                break
            decoded = ord(byte) ^ key
            f2.write(bytes([decoded]))
    subprocess.run(["notepad.exe", target])
