"""Static-only mutation controls; never execute the supplied PE.

Usage: python3 check.py SAMPLE SCRATCH_DIRECTORY
Requires the reviewed b35753a34ae1 sample and cleave on PATH.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
DRIVER = "micro-behaviors/os/kernel/driver::x86-demand-driver-service-calls"
IMPORTED = "micro-behaviors/os/service/create::create-service-w-import"
NAMED = "micro-behaviors/os/service/create::create-service-w-reference"
SHELL = "micro-behaviors/process/create/shell/spawn::shell-execution-comp"
IE = "micro-behaviors/process/info/name::iexplore-exe-name"
PROFILE = "micro-behaviors/os/kernel/driver::unsigned-privileged-service-driver-api-set"
OLD_IE = "metadata/file/string/application-name::iexplore-executable-name"
RUNDLL = "metadata/lang/source/syntax/command::rundll32-command-syntax-reference"


def main():
    source, scratch = map(Path, sys.argv[1:])
    original = source.read_bytes()
    assert hashlib.sha256(original).hexdigest() == (
        "b35753a34ae16e80d1f8783067c8f533ef242ee1b0f3791bfd103f8b886c3503"
    )
    scratch.mkdir(parents=True, exist_ok=True)
    # Offsets identify mutation sites only; the detection binds the actual IAT
    # addresses and service-type constants without requiring these offsets.
    assert original[0xb90:0xb9a] == bytes.fromhex("6a006a006a006a006a00")
    assert original[0xba2] == 3 and original[0xba4] == 1
    assert original[0xbda:0xbe1] == bytes.fromhex("6a006a0056ff15")
    cases = []

    def add(name, data, present, absent):
        path = scratch / (name + ".exe")
        path.write_bytes(data)
        cases.append((path, set(present), set(absent)))

    add("original", original, [DRIVER, IMPORTED, IE, PROFILE], [NAMED, SHELL, OLD_IE])
    for name, offset, value in [
        ("user-mode-service", 0xba4, 0x10),
        ("auto-start-driver", 0xba2, 2),
    ]:
        data = bytearray(original)
        data[offset] = value
        add(name, data, [IMPORTED], [DRIVER, NAMED, SHELL])
    for name, offset, target in [
        ("wrong-create-api", 0xbaf, 0x40a008),
        ("wrong-start-api", 0xbe1, 0x40a024),
    ]:
        data = bytearray(original)
        struct.pack_into("<I", data, offset, target)
        add(name, data, [IMPORTED], [DRIVER, NAMED])
    data = bytearray(original)
    data[0xbda:0xbe7] = b"\x90" * 13
    add("no-start-call", data, [IMPORTED], [DRIVER, NAMED])
    data = original.replace(b"CreateServiceW\0", b"CreateServiceX\0")
    data += b"\0CreateServiceW\0"
    add("name-without-import", data, [NAMED, PROFILE], [DRIVER, IMPORTED])
    add("large-imported-image", original.ljust(2700000, b"\0"),
        [DRIVER, IMPORTED], [NAMED])
    data = original.replace(b"safemon.dll hook2", b"safemon.dll,hook2")
    assert data != original
    add("comma-export-command", data, [RUNDLL, DRIVER], [SHELL])
    data = original.replace(b"IEXPLORE.EXE", b"XEXPLORE.EXE")
    data = data.replace(b"iexplore.exe", b"xexplore.exe")
    data = data.replace("IEXPLORE.EXE".encode("utf-16le"),
                        "XEXPLORE.EXE".encode("utf-16le"))
    data = data.replace("iexplore.exe".encode("utf-16le"),
                        "xexplore.exe".encode("utf-16le"))
    add("no-ie-name", data, [DRIVER], [IE, OLD_IE])

    def check(case):
        path, present, absent = case
        result = subprocess.run(
            ["cleave", "--traits-dir", str(ROOT), "--format", "json", str(path)],
            check=True, capture_output=True, text=True,
        )
        report = json.loads(result.stdout)
        # Check this image, not a string or behavior in an embedded child.
        traits = {item["id"] for item in report["files"][0]["traits"]}
        missing, unexpected = present - traits, absent & traits
        assert not missing and not unexpected, (path.name, missing, unexpected)
        return {"case": path.stem, "present": sorted(present),
                "absent": sorted(absent), "passed": True}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
