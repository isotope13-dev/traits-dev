"""Static-blob decode with no encode half: the decoder input was authored
elsewhere, so this is not a round trip. The transport leg and the
transport-context exception MUST NOT match here.
"""
import os


def run_staged_payload() -> None:
    os.system("echo 'aGVsbG8td29ybGQ=' | base64 -d | bash")
