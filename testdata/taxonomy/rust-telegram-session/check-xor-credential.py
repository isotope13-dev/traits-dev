#!/usr/bin/env python3
"""Check credential-decoder bindings and their session-theft consumers."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ENCODING = "objectives/anti-static/obfuscation/string/encoding::"
STEALER = "objectives/exfiltration/stealer/token::"
ATOM = ENCODING + "rust-xor-macro-bot-credential"
CONCEALMENT = ENCODING + "rust-session-theft-xor-credential-concealment"
UPLOAD = STEALER + "rust-telegram-session-archive-upload"
XOR_UPLOAD = STEALER + "rust-xor-bot-session-archive-upload"


def main():
    original = (HERE / "renamed.rs").read_text()
    plain_bot = 'let bot = Bot::new("9999999999:abcdefghijklmnopqrstuvwxyzABCDE12345");'
    token = b"9999999999:abcdefghijklmnopqrstuvwxyzABCDE12345"
    numbers = ", ".join(str(b ^ 0xAA) for b in token)
    encoded_bot = (f"let encoded = vec![{numbers}];\n"
                   "    let credential = ut!(encoded);\n"
                   "    let bot = Bot::new(credential);")
    positive = original.replace(plain_bot, encoded_bot)
    assert positive != original
    examples = {
        "positive.rs": (positive, True, True),
        "renamed.rs": (positive.replace("macro_rules! ut", "macro_rules! decode_renamed")
                       .replace("ut!(", "decode_renamed!(")
                       .replace("encoded", "字节列表")
                       .replace("credential", "凭证")
                       .replace("KEY", "mask_renamed")
                       .replace("0xAA", "0x37"), True, True),
        "hex-vector.rs": (positive.replace(numbers, ", ".join(hex(b ^ 0xAA) for b in token)), True, True),
        "formatted.rs": (positive.replace(".map(|&b| b ^ KEY).collect()",
                                         ".map ( |&b|\n b^KEY )\n.collect ()"), True, True),
        "different-chat.rs": (positive.replace("-1009999999999", "-1008888888888"), True, True),
        "wrong-macro.rs": (positive.replace("ut!(encoded)", "other!(encoded)"), False, True),
        "wrong-bytes.rs": (positive.replace("ut!(encoded)", "ut!(other_bytes)"), False, True),
        "wrong-token.rs": (positive.replace("Bot::new(credential)", "Bot::new(other_token)"), False, True),
        "wrong-decoded-value.rs": (positive.replace("from_utf8(deobfuscated)", "from_utf8(other_bytes)"), False, True),
        "commented-xor.rs": (positive.replace("b ^ KEY", "b /* ^ KEY */"), False, True),
        "quoted-xor.rs": (positive.replace("b ^ KEY", '"b ^ KEY"'), False, True),
        "unrelated-utf8.rs": (positive.replace("String::from_utf8(deobfuscated)",
                                               'Other::conversion(deobfuscated) /* String::from_utf8(deobfuscated) */'), False, True),
        "plain-token.rs": (original, False, True),
        "ordinary-upload.rs": ((HERE / "ordinary-upload.rs").read_text(), False, False),
        "backup-only.rs": ((HERE / "backup-only.rs").read_text(), False, False),
        "comments-only.rs": ("/*\n" + positive + "\n*/\nfn main() {}\n", False, False),
        "encoded-ordinary-upload.rs": ((HERE / "ordinary-upload.rs").read_text()
                                       .replace(plain_bot, encoded_bot), True, False),
    }
    with tempfile.TemporaryDirectory(prefix="xor-bot-credential-") as tmp:
        folder = Path(tmp)
        for name, (source, _, _) in examples.items():
            (folder / name).write_text(source)
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--json", str(folder)],
            capture_output=True, text=True, check=True,
            env=dict(os.environ, CLEAVE_SKIP_CACHE="1"))
        reports = [f for line in result.stdout.splitlines()
                   for f in json.loads(line)["files"]]
        seen = set()
        for report in reports:
            name = Path(report["path"]).name
            if name not in examples:
                continue
            seen.add(name)
            _, atom, upload = examples[name]
            traits = {t["id"]: t["crit"] for t in report.get("traits", [])}
            for rule, expected in ((ATOM, atom), (UPLOAD, upload),
                                   (CONCEALMENT, atom and upload),
                                   (XOR_UPLOAD, atom and upload)):
                assert (rule in traits) == expected, (name, rule, expected, traits)
            if atom and upload:
                assert all(traits[rule] == 5 for rule in (UPLOAD, XOR_UPLOAD, CONCEALMENT))
            if name in {"ordinary-upload.rs", "comments-only.rs"}:
                assert not any(c >= 4 for c in traits.values()), (name, traits)
            if name in {"backup-only.rs", "encoded-ordinary-upload.rs"}:
                assert not any(c == 5 for c in traits.values()), (name, traits)
        assert seen == examples.keys(), (seen, examples.keys())
    print(json.dumps({"cases": len(examples), "status": "pass"}))


if __name__ == "__main__":
    main()
