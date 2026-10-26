"""This control contains an actual Mimikatz command argument. It must remain
visible to the command-reference matchers regardless of whether the file also
contains an embedded detection rule. The fixture is analyzed statically and
must never be launched during validation.
"""
import subprocess
subprocess.run(["mimikatz.exe", "sekurlsa::logonpasswords"])
