import os


def fetch():
    os.system("curl -s -o /tmp/archive.tgz http://x.invalid/archive.tgz")
