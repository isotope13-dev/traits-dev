"""Validate source-bound attack coverage without executing specimens."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        document, end = decoder.raw_decode(text.lstrip())
        yield document
        text = text.lstrip()[end:]


def scan(paths, destination):
    run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir',
                          str(ROOT), '--format', 'json', *map(str, paths)],
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    destination.write_text(run.stdout)
    return [f for d in documents(run.stdout) for f in d['files']]


def check(rows):
    reports = {Path(r['path']).name: r for r in rows}
    traits = {n: {t['id'] for t in r.get('traits', [])} for n, r in reports.items()}
    hostile = {n: {t['id'] for t in r.get('traits', []) if t['crit'] == 5}
               for n, r in reports.items()}
    calendar = 'objectives/execution/payload/interpreter-stdin::icloud-calendar-shell-deaddrop'
    resign = 'objectives/evasion/security-bypass/codesign::downloaded-app-adhoc-resign-launch'
    macro = 'objectives/execution/interpreter/document::hidden-xlm-regsvr32-command-staging'
    spray = 'objectives/lateral-movement/brute-force/password/web::microsoft-oauth-password-spray'
    for name in ['calendar-renamed.sh', 'sign-unrelated-app.sh', 'calendar-inline.sh']:
        assert calendar in hostile[name], name
    assert 'objectives/execution/payload/script-eval::icloud-calendar-shell-eval' in hostile['calendar-eval.sh']
    assert resign in hostile['calendar-renamed.sh']
    assert resign not in hostile['sign-unrelated-app.sh']
    for name in ['calendar-read-only.sh', 'calendar-unrelated-shell.sh',
                 'sign-only-installer.sh', 'sign-no-open.sh', 'macro-creation.vbs',
                 'macro-hidden-dispatch.vbs', 'macro-visible-command.vbs',
                 'macro-hide-only.vbs', 'single-login.go', 'single-login.py',
                 'font-preview.sh', 'encrypted-installer.sh',
                 'evaluator-reference.lnk', 'ordinary-arguments.lnk', 'calendar-unrelated-eval.sh']:
        assert not hostile[name], (name, hostile[name])
    for name in ['macro-renamed-command.vbs', 'xlm-register-download-dropper.vbs']:
        assert macro in hostile[name], name
    assert len(hostile['macro-msbuild-shellexec-dropper.py']) >= 1
    assert len(hostile['tradertraitor-safari-updater.sh']) >= 4
    for name in ['spray-localized.go', 'localized.py', 'localized.ts']:
        assert spray in hostile[name], name
    ref = 'metadata/lang/source/naming/action::lnk-invoke-expression-reference'
    assert ref in traits['evaluator-reference.lnk']
    assert ref not in traits['ordinary-arguments.lnk']
    assert 'micro-behaviors/fs/attributes/xattr::xattr-clear' in traits['sign-only-installer.sh']
    assert 'micro-behaviors/data/collection/create::excel4-macro-sheet-creation' in traits['macro-creation.vbs']
    return len(rows)


if __name__ == '__main__':
    paths = [ROOT / p for p in json.loads((HERE / 'control-paths.json').read_text())]
    rows = scan(paths, HERE / 'controls-after.json')
    print(f'Passed {check(rows)} controls, including existing attack fixtures')
