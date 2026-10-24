"""Stage controls outside test paths so testing-context exclusions cannot win.

Usage: python3 check.py --scratch /absolute/scratch --oxlint /path/to/oxlint
The ELF controls are matcher fixtures, not recovered malware or executed code.
"""
import argparse
import base64
import json
from pathlib import Path
import shutil
import struct
import subprocess


def elf_fixture(interpreter=False):
    names = b"\0.text\0.rodata\0.shstrtab\0.interp\0"
    data = bytearray(0x300)
    code = bytes.fromhex("b83c00000031ff0f05")
    strings = b"reference\0__chmod\0execl\0unlink\0/tmp/.key\0/tmp/.cipher\0/tmp/.output\0"
    data[0x100:0x100 + len(code)] = code
    data[0x120:0x120 + len(strings)] = strings
    data[0x200:0x200 + len(names)] = names
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (1, 1, 6, 0x400100, 0x100, len(code), 0, 0, 16, 0),
                (7, 1, 2, 0x400120, 0x120, len(strings), 0, 0, 1, 0),
                (15, 3, 0, 0, 0x200, len(names), 0, 0, 1, 0)]
    if interpreter:
        path = b"/lib64/ld-linux-x86-64.so.2\0"
        data[0x240:0x240 + len(path)] = path
        sections.append((25, 1, 2, 0x400240, 0x240, len(path), 0, 0, 1, 0))
        data[120:176] = struct.pack("<II6Q", 3, 4, 0x240, 0x400240,
                                    0x400240, len(path), len(path), 1)
    for section in sections:
        data.extend(struct.pack("<II4QII2Q", *section))
    data[:64] = struct.pack("<16sHHIQQQIHHHHHH", b"\x7fELF\x02\x01\x01" + bytes(9),
                           2, 62, 1, 0x400100, 64, 0x300, 0, 64, 56,
                           2 if interpreter else 1, 64, len(sections), 3)
    data[64:120] = struct.pack("<II6Q", 1, 5, 0, 0x400000, 0x400000,
                              len(data), len(data), 0x1000)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", required=True, type=Path)
    parser.add_argument("--oxlint", required=True, type=Path)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    staged = args.scratch / "controls-final"
    staged.mkdir(parents=True, exist_ok=True)
    key = 'AWS_ACCESS_KEY_ID = "AKIAQ7M8K2X9P4W6T3Y1"\n'
    example = "/*\n```js\nconst " + key + "```\n*/\n"
    sources = {
        "live.py": key,
        "fenced.js": example,
        "mixed.js": example + key,
        "encoded.py": 'import base64\nvalue = base64.b64decode("' +
                      base64.b64encode(key.encode()).decode() + '")\n',
        "synthetic.py": 'aws_access_key = "AKIA1111111111111111"\n' +
                        'aws_access_key_id = "AKIA1234567890123456"\n',
        "s3-compatible.py": key.replace("AWS_ACCESS_KEY_ID", "MINIO_ACCESS_KEY"),
    }
    for name, source in sources.items():
        (staged / name).write_text(source)
    shutil.copy(repo / "testdata/simple-stealer/08-linux-aws-credentials.py",
                staged / "existing-aws-stealer.py")
    (staged / "static-name-reference").write_bytes(elf_fixture())
    (staged / "dynamic-name-reference").write_bytes(elf_fixture(True))
    original = args.oxlint.read_bytes()
    (staged / "oxlint-plus-key").write_bytes(original + b"\0" + key.encode() + b"\0")
    (staged / "oxlint-plus-decoded-key").write_bytes(
        original + b"\0" + base64.b64encode(key.encode()) + b"\0")
    result = subprocess.run([args.cleave, "--traits-dir", str(repo), "--disable",
                             "radare2", "--json", str(staged)],
                            check=True, capture_output=True, text=True)
    (args.scratch / "controls-final.jsonl").write_text(result.stdout)
    files = {Path(f["path"]).name: {t["id"] for t in f.get("traits", [])}
             for line in result.stdout.splitlines()
             for f in json.loads(line)["files"]}
    prefix = "micro-behaviors/data/format/credentials::"
    for name in ["live.py", "mixed.js", "encoded.py"]:
        assert prefix + "aws-key-assignment" in files[name], name
    for name in ["fenced.js", "synthetic.py", "s3-compatible.py"]:
        assert not any("aws-key-assignment" in t for t in files[name]), name
    assert prefix + "native-aws-key-assignment" in files["oxlint-plus-key"]
    assert prefix + "native-decoded-aws-key-assignment" in files["oxlint-plus-decoded-key"]
    chmod = "micro-behaviors/fs/chmod/modify::static-chmod-symbol-text"
    assert chmod in files["static-name-reference"]
    assert chmod not in files["dynamic-name-reference"]
    assert "objectives/command-and-control/dropper/staging/temp::static-hidden-tmp-payload-exec-stub" in files["static-name-reference"]
    for rule in ["credential-file-content-http-export", "python-credential-http-upload"]:
        assert "objectives/exfiltration/stealer/credential::" + rule in files["existing-aws-stealer.py"]
    print(f"PASS: {len(files)} controls; assignments, decoded keys, theft, and static-loader coverage retained")


if __name__ == "__main__":
    main()
