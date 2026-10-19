"""Check the named positive and near-miss observations in cases.json."""
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

root=Path(__file__).resolve().parents[3]
cases=json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
engine=sys.argv[1] if len(sys.argv)>1 else "cleave"

def check(case):
    result=subprocess.run([engine,"--traits-dir",str(root),"--format","json",
                           str(root/case["path"])],capture_output=True,text=True)
    if result.returncode:
        return [case["path"]+": "+result.stderr[-2000:]]
    try:
        files=json.loads(result.stdout)["files"]
        actual={t["id"] for f in files for t in f.get("traits",[])}
    except (ValueError,KeyError) as exc:
        return [case["path"]+": invalid report: "+str(exc)]
    errors=[]
    for trait in case["matched"]:
        if trait not in actual:errors.append(case["path"]+": missing "+trait)
    for trait in case["not_matched"]:
        if trait in actual:errors.append(case["path"]+": unexpected "+trait)
    return errors

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    errors=[e for result in pool.map(check,cases) for e in result]
for e in errors:print(e)
print(str(len(cases))+" fixtures; "+str(len(errors))+" failures")
sys.exit(bool(errors))
