import argparse
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument("--command", choices=["list"], default="list")
args = parser.parse_args()
lock_meta = "LOCK_NAME=PRODUCT\n"
image = "upgradepkg.tar"
endpoint = "/cgi-bin/tool_reprogramming.cgi"
content_type = "multipart/form-data"

def describe(name, body, mode):
    print(name, body, oct(mode))

with tarfile.open("vendor.pkg", mode="r") as archive:
    print(archive.getnames())
    describe("pre", "expected maintenance hook", 0o755)
