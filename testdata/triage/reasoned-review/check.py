"""Run controls outside test-named paths so fixture exclusions cannot pass them."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix="trait-control-") as temporary:
    for filename, expected in [("prompt-defense.js", 0), ("ordinary-build.js", 0), ("ordinary-bootstrap.cmd", 0), ("prompt-override.js", 2)]:
        target = Path(temporary) / ("input" + Path(filename).suffix)
        shutil.copyfile(fixtures / filename, target)
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--format", "json", "analyze", str(target)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr
        assert not result.stderr.strip(), result.stderr
        report = json.loads(result.stdout)
        traits = report["files"][0]["traits"]
        hostile = [trait for trait in traits if trait["crit"] == 5]
        suspicious = [trait for trait in traits if trait["crit"] == 4]
        assert not hostile, (filename, hostile)
        assert len(suspicious) == expected, (filename, suspicious)
        if expected:
            assert {trait["id"] for trait in suspicious} == {
                "objectives/evasion/security-bypass/llm/persona::llm-unrestricted-persona",
                "objectives/evasion/security-bypass/llm/override::llm-prior-instruction-override",
            }
        print(f"PASS {filename}: 0 hostile, {expected} suspicious")
