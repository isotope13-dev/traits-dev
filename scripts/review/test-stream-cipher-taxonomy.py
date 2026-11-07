#!/usr/bin/env python3
"""Check stream-cipher naming and source-size boundaries without running samples."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    salsa = "micro-behaviors/crypto/symmetric/salsa::salsa20-stream-cipher-call"
    xsalsa = "micro-behaviors/crypto/symmetric/salsa::xsalsa20-stream-cipher-call"
    chacha = "micro-behaviors/crypto/symmetric/stream/chacha::chacha20-stream-cipher-call"
    chacha_operation = "micro-behaviors/crypto/symmetric/stream/chacha::chacha20-cipher-operation"
    sigma = "micro-behaviors/crypto/symmetric/stream/sigma::chacha-salsa-constant"
    transformed = "micro-behaviors/crypto/symmetric/stream/chacha::transformed-response-returned"
    js = (
        'const f = (response) => { const decoded = Buffer.from(response.data, "base64"); '
        'const transformed = xchacha20(key, nonce, decoded); resolve(transformed); };\n'
    )
    catalog = "".join(
        f"Package: item{i}\nFilename: pool/item{i}.deb\nSHA256: {'a' * 64}\n"
        for i in range(3)
    )
    cases = {
        "salsa.c": ("void sample(void *p) { salsa20_crypt(p); }\n", {salsa}, {xsalsa, chacha, chacha_operation}),
        "xsalsa.c": ("void sample(void *p) { crypto_stream_xsalsa20_xor(p); }\n", {xsalsa}, {salsa, chacha, chacha_operation}),
        "chacha.c": ("void sample(void *p) { crypto_stream_chacha20_xor(p); }\n", {chacha}, {salsa, xsalsa}),
        "sigma.c": ('const char *key = "expand 32-byte k";\n', {sigma}, {salsa, xsalsa, chacha, chacha_operation}),
        "salsa-catalog.kt": (
            'val archive = """\n' + catalog + '"""\nfun sample() { salsa20_crypt(data) }\n',
            {salsa, "metadata/file/catalog/package::debian-packages-index"},
            {xsalsa, chacha},
        ),
        "small.js": (js, {transformed}, set()),
        "large.js": (" " * 140000 + js, {transformed}, set()),
    }
    with tempfile.TemporaryDirectory(prefix="stream-cipher-taxonomy-") as tmp:
        paths = []
        for name, (source, _, _) in cases.items():
            path = Path(tmp) / name
            path.write_text(source)
            paths.append(str(path))
        result = subprocess.run(
            [str((repo / args.cleave).resolve()), "--traits-dir", str(repo), "--format=json", *paths],
            check=True,
            capture_output=True,
            text=True,
        )
        reports = [json.loads(line) for line in result.stdout.splitlines() if line]
        roots = {Path(report["files"][0]["path"]).name: report["files"][0] for report in reports}
        assert set(roots) == set(cases), (set(roots), set(cases))
        for name, (_, required, forbidden) in cases.items():
            ids = {trait["id"] for trait in roots[name].get("traits", [])}
            assert required <= ids, (name, "missing", required - ids)
            assert not forbidden & ids, (name, "unexpected", forbidden & ids)
            print("PASS", name)


if __name__ == "__main__":
    main()
