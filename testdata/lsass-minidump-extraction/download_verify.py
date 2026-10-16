"""Installer download integrity check (negative control)."""
import hashlib

EXPECTED_SHA1 = "abdcba254aec226bb7762f709753084d3985b7d3"


def verify_installer(path):
    digest = hashlib.sha1(open(path, "rb").read()).hexdigest()
    if digest != EXPECTED_SHA1:
        raise SystemExit("installer hash mismatch")
    return True
