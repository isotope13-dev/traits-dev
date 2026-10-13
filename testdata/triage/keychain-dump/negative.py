import os

# Builder documents the argv shape but never launches it: suspicious command
# reference only, no executed secret extraction.
DUMP_ARGV = ["security", "dump-keychain", "-d", os.path.expanduser(
    "~/Library/Keychains/login.keychain-db")]


def describe():
    return " ".join(DUMP_ARGV[:3])
