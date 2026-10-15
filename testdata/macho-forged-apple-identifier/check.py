"""Forged Apple platform identity controls; never execute an image.

An ad-hoc signature is self-signed: anyone can stamp any CodeDirectory
identifier, including `com.apple.*`. `metadata/signed/platform::apple`
must therefore require a certificate chain anchoring at Apple, not just
the identifier prefix, or every forged identifier suppresses
platform-gated findings (and the packed-command-runner composites that
need them) across the corpus.

Run from the repository root:

python3 testdata/macho-forged-apple-identifier/check.py --cleave <cleave>

No specimen bytes are checked into this repository. The forged mutant is
generated at runtime from an in-repo ad-hoc fixture by same-length byte
replacement, so all file offsets are preserved.
"""
import argparse
import json
import pathlib
import subprocess
import tempfile

APPLE = 'metadata/signed/platform::apple'
PREFIX = 'metadata/binary/signing::apple-identifier-prefix'
FORGED = 'objectives/evasion/masquerade/trust::adhoc-forged-apple-platform-identity'
ADHOC = 'metadata/signed/trust-level::adhoc'

FIXTURE = pathlib.Path('testdata/taxonomy/browser-export-final/adhoc-notes-client.macho')
OLD_ID = b'adhoc-notes-client.macho\x00'
NEW_ID = b'com.apple.notes-client\x00\x00\x00'
assert len(OLD_ID) == len(NEW_ID)

# Best-effort genuine-Apple positive control (darwin hosts only). Eligibility
# is derived from independent evidence (a verified Apple chain anchor), never
# from the rule under test.
POSITIVE_CANDIDATES = ['/bin/ls', '/usr/bin/sw_vers', '/bin/echo', '/bin/sh']


def scan(cleave, traits_dir, path):
    run = subprocess.run([cleave, '--traits-dir', traits_dir, '--format=json', str(path)],
                         capture_output=True, text=True, check=True)
    report = json.loads(run.stdout)
    files = report['files'] if 'files' in report else report['raw']['files']
    return {t['id'] for t in files[0]['traits']}


def facts(cleave, path):
    run = subprocess.run([cleave, 'facts', str(path)], capture_output=True, text=True, check=True)
    return json.loads(run.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cleave', required=True)
    ap.add_argument('--traits-dir', default='.')
    args = ap.parse_args()

    cases = []
    with tempfile.TemporaryDirectory() as tmp:
        original = FIXTURE.read_bytes()
        assert original.count(OLD_ID) == 1
        base = pathlib.Path(tmp) / 'adhoc-notes-client.macho'
        base.write_bytes(original)
        cases.append(('adhoc-fixture', base,
                      {APPLE: False, PREFIX: False, FORGED: False, ADHOC: True}))

        forged = pathlib.Path(tmp) / 'forged-apple-identifier.macho'
        forged.write_bytes(original.replace(OLD_ID, NEW_ID))
        cases.append(('forged-apple-identifier', forged,
                      {APPLE: False, PREFIX: True, FORGED: True, ADHOC: True}))

        positive = None
        for candidate in POSITIVE_CANDIDATES:
            p = pathlib.Path(candidate)
            if not p.exists():
                continue
            try:
                cs = facts(args.cleave, p)['values']['macho']['code_signature']
            except Exception:
                continue
            if cs.get('cms', {}).get('chain_anchor') == 'apple':
                positive = p
                break
        if positive is not None:
            cases.append(('genuine-apple-binary', positive,
                          {APPLE: True, PREFIX: True, FORGED: False}))
        else:
            print(json.dumps({'case': 'genuine-apple-binary', 'skipped': True,
                              'reason': 'no Apple-signed Mach-O on this host'}))

        passed = 0
        for name, path, expectations in cases:
            found = scan(args.cleave, args.traits_dir, path)
            actual = {i: i in found for i in expectations}
            ok = actual == expectations
            passed += ok
            print(json.dumps({'case': name, 'pass': ok,
                              **({} if ok else {'actual': actual, 'expected': expectations})}),
                  flush=True)
        print(json.dumps({'passed': passed, 'total': len(cases)}))
        if passed != len(cases):
            raise SystemExit(1)


if __name__ == '__main__':
    main()
