"""Check static traits without running the fixture programs."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main():
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
    for case in cases:
        result = subprocess.run(
            ["cleave", "--traits-dir", str(ROOT), "--format", "json", case["path"]],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        traits = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
        missing = set(case["matched"]) - traits.keys()
        unexpected = set(case["not_matched"]) & traits.keys()
        assert not missing and not unexpected, (case["path"], missing, unexpected)
        for key, severity in case.get("criticalities", {}).items():
            assert traits[key]["crit"] == severity, (key, traits[key])
        print("PASS", case["path"], flush=True)


if __name__ == "__main__":
    main()
