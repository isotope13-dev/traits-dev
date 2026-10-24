"""Scan inert controls outside testdata so testing-path exclusions cannot mask them."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--scratch", required=True, type=Path)
args = parser.parse_args()

OBF = "objectives/anti-static/obfuscation/obfuscator/signature::"
PACKED = "objectives/anti-static/obfuscation/eval/scripting/decode::"
WEBHOOK = "micro-behaviors/communications/http/webhook::"
KEY = "micro-behaviors/crypto/key/generate::"
BUILD = "metadata/build/manifest::"
EXEC = "micro-behaviors/process/create/shell/command-string::"
LOL = "objectives/execution/lolbin/frameworks::"
SYNTAX = "metadata/lang/source/syntax/call/invocation::python-add-file-member-call"
SUBPROCESS = "micro-behaviors/process/create/subprocess::run-ast"
cases = {
    "legacy-runtime.py": {
        "required": {OBF + "pyarmor-signature-core": 4, SUBPROCESS: 3},
    },
    "modern-runtime.py": {"required": {OBF + "pyarmor-signature-core": 4}},
    "runtime-call.py": {
        "required": {OBF + "pyarmor-signature-core": 4, OBF + "pyarmor-runtime-call": 4},
    },
    "build-helper.py": {
        "required": {SUBPROCESS: 3},
        "absent": [OBF + "pyarmor-signature-core", PACKED + "python-packed-subprocess"],
        "max": 3,
    },
    "ordinary-add-file.py": {
        "required": {SYNTAX: 3},
        "absent": [WEBHOOK + "python-discord-webhook-add-file"],
    },
    "webhook-add-file.py": {
        "required": {SYNTAX: 3, WEBHOOK + "python-discord-webhook-add-file": 3},
    },
    "keylog-upload.py": {
        "required": {
            "objectives/exfiltration/stealer/input::python-keylog-discord-file-upload": 5,
        },
    },
    "key-generation.py": {
        "required": {KEY + "fernet-keygen-call": 3, KEY + "fernet-keygen-text": 3},
        "max": 3,
    },
    "inplace-encryption.py": {
        "required": {
            KEY + "fernet-keygen-call": 3,
            KEY + "fernet-keygen-text": 3,
            "objectives/impact/ransom/encrypt/filesystem::inplace-encrypt": 5,
            "objectives/impact/wipe/disk/crypto::fernet-wiper-ransomware": 5,
        },
    },
    "normal-build.csproj": {
        "required": {
            BUILD + "msbuild-copy-sources": 3,
            BUILD + "msbuild-makedir-task": 3,
            EXEC + "msbuild-exec-command": 3,
        },
        "max": 3,
    },
    "design-time-exec.csproj": {
        "required": {
            LOL + "getframeworkpaths-design-time-exec": 5,
            LOL + "getframeworkpaths-stage-and-launch": 5,
        },
    },
}

with tempfile.TemporaryDirectory(prefix="trait-controls-", dir=args.scratch) as tmp:
    for name in cases:
        shutil.copyfile(HERE / name, Path(tmp) / name)
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json", tmp],
        check=True, text=True, capture_output=True,
    )
    reports = {}
    for line in result.stdout.splitlines():
        for file in json.loads(line).get("files", []):
            reports[Path(file["path"]).name] = {
                trait["id"]: trait["crit"] for trait in file.get("traits", [])
            }
    for name, case in cases.items():
        traits = reports[name]
        for trait, crit in case.get("required", {}).items():
            assert traits.get(trait) == crit, (name, trait, traits.get(trait))
        assert not set(case.get("absent", [])).intersection(traits), name
        if "max" in case:
            assert max(traits.values(), default=0) <= case["max"], (name, traits)
print(f"PASS: {len(cases)} PyArmor, file attachment, key generation and MSBuild controls")
