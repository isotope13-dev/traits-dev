#!/usr/bin/env python3
"""Check name reconstruction versus quoted data and request execution statically."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REVERSE = "objectives/anti-static/obfuscation/string/reverse::php-reconstructs-reversed-decoder-name"
RETIRED = {
    "objectives/command-and-control/backdoor/webshell/decoder::reversed-dangerous-php--rx-8",
    "objectives/command-and-control/backdoor/webshell/decoder::php-tiny-reversed-decoder-eval-stub",
    "third_party/SigBase/APT/Webshell/Tiny",
}
CASES = {
    "inert.php": ('<?php eval(strrev("edoced_46esab"));\n', True),
    "renamed.php": ('<?php eval(strrev("edoced_46esab"));\n', True),
    "inflate.php": ("<?php $decoder = strrev('etalfnizg');\n", True),
    "mixed-case.php": ("<?php $decoder = STRREV('EDOCED_46ESAB');\n", True),
    "qualified.php": ("<?php $decoder = \\strrev('etalfnizg');\n", True),
    "ordinary-reverse.php": ("<?php echo strrev('hello');\n", False),
    "literal.php": ("<?php $label = 'edoced_46esab';\n", False),
    "quoted-call.php": ('<?php echo \'strrev("edoced_46esab")\';\n', False),
    "comment.php": ('<?php /* strrev("edoced_46esab") */\n', False),
    "longer-token.php": ("<?php echo strrev('xetalfnizgx');\n", False),
    "constant-eval.php": ("<?php eval('echo 1;');\n", False),
    "request.php": ("<?php eval($_POST['code']);\n", False),
    "decoded-request.php": ("<?php eval(base64_decode($_POST['code']));\n", False),
}


def main():
    # Keep generated paths outside testdata: broad test-directory exclusions
    # would otherwise suppress execution findings and invalidate these checks.
    with tempfile.TemporaryDirectory(dir=ROOT, prefix="php-reversal-controls-") as directory:
        for name, (source, _) in CASES.items():
            (Path(directory) / name).write_text(source)
        command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
                   "--format", "json", directory]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        decoder = json.JSONDecoder()
        remaining = result.stdout
        reports = {}
        while remaining.strip():
            report, end = decoder.raw_decode(remaining.lstrip())
            remaining = remaining.lstrip()[end:]
            for file in report["files"]:
                reports[Path(file["path"]).name] = file.get("traits", [])
        for name, (_, expected) in CASES.items():
            traits = reports[name]
            ids = {trait["id"] for trait in traits}
            assert (REVERSE in ids) == expected, (name, ids)
            assert not (ids & RETIRED), (name, ids & RETIRED)
            hostile = [trait for trait in traits if trait["crit"] == 5]
            suspicious = [trait for trait in traits if trait["crit"] == 4]
            if name == "decoded-request.php":
                assert hostile, (name, traits)
                assert any("webshell" in trait["id"] for trait in hostile)
            elif name == "request.php":
                assert "objectives/execution/interpreter/eval/remote::eval-user-input" in ids
            else:
                assert not hostile, (name, hostile)
                assert len(suspicious) == int(expected), (name, suspicious)
        print(f"Passed {len(CASES)} controls, including a live request-to-eval surface.")


if __name__ == "__main__":
    main()
