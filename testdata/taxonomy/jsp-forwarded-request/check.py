#!/usr/bin/env python3
"""Scan all controls together and assert binding and placement results."""
import json, os, subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[3]
cases=json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
run=subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--disable", "third-party", "--format", "json", *[str(root/c["path"]) for c in cases]], text=True, capture_output=True, cwd=root)
if run.returncode: raise SystemExit(run.stderr)
decoder=json.JSONDecoder()
reports=[]
remaining=run.stdout.strip()
while remaining:
 report,end=decoder.raw_decode(remaining)
 reports.append(report)
 remaining=remaining[end:].lstrip()
files={str(Path(f["path"]).resolve()):f for report in reports for f in report["files"]}
for c in cases:
 f=files[str((root/c["path"]).resolve())]
 observed={t["id"] for t in f.get("traits", [])}
 missing=set(c["matched"])-observed
 extra=set(c["not_matched"])&observed
 assert not missing and not extra, (c["path"], "missing", missing, "unexpected", extra)
 if not any(t.startswith("objectives/") for t in c["matched"]):
  assert not [t for t in f.get("traits",[]) if t["crit"]==5], (c["path"], "unexpected hostile")
print(f"Passed {len(cases)} JSP, ASP.NET and placement controls")
