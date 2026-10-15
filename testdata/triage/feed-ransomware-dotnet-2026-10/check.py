"""Third-party family-label consolidation controls; never execute an image.

Two SigBase YARA rules fire on generic strings that unrelated malware also
carries, misattributing the family at hostile weight:

- Winnti/Sample/May18 needs only the wide strings "wireshark"+"procexp",
  which also occur in ransomware analysis-tool blocklists.
- CN/Disclosed/20180208/Mal1 fires on one ubiquitous IE6 User-Agent string
  that unrelated downloaders also send.

third-party/config.yaml suppresses each when the native finding explains
the match. This check pins that behavior on the triage specimens.

python3 check.py --cleave <cleave> [--source <samples-root>]
No specimen bytes are checked into this repository.
"""
import argparse
import json
import pathlib
import subprocess

WINNTI = 'third_party/SigBase/Winnti/Sample/May18'
DOTNET_RANSOM = 'objectives/impact/ransom/encrypt-dotnet::dotnet-ransomware-encryptor'
FODHELPER = 'objectives/privilege-escalation/elevation-control/uac-bypass/hijack::fodhelper-delegateexecute-hijack'
CN_MAL1 = 'third_party/SigBase/CN/Disclosed/20180208/Mal1'
STORM = 'well-known/malware/botnet/stormattack::stormattack-servicedll-injection-dropper'

CASES = [
    ('266da0bc77cc/xoilaczsxz.us.com_nano.exe',
     {DOTNET_RANSOM: True, FODHELPER: True, WINNTI: False}),
    ('48d8a75ec157/xoilaczsxz.us.com_hyber.exe',
     {DOTNET_RANSOM: True, WINNTI: False}),
    ('8e002cc1d2d5/2026-10-14_0bf443395e45e71a9c51cf65f9c79cd1_elex_remcos_wannacry',
     {STORM: True, CN_MAL1: False}),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cleave', required=True)
    ap.add_argument('--traits-dir', default='.')
    ap.add_argument('--source', type=pathlib.Path,
                    default=pathlib.Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-45f6194b/samples'))
    args = ap.parse_args()

    passed = 0
    for rel, expectations in CASES:
        path = args.source / rel
        run = subprocess.run([args.cleave, '--traits-dir', args.traits_dir,
                              '--format=json', str(path)],
                             capture_output=True, text=True, check=True)
        report = json.loads(run.stdout)
        files = report['files'] if 'files' in report else report['raw']['files']
        found = {t['id'] for t in files[0]['traits']}
        actual = {i: i in found for i in expectations}
        ok = actual == expectations
        passed += ok
        print(json.dumps({'case': rel, 'pass': ok,
                          **({} if ok else {'actual': actual, 'expected': expectations})}),
              flush=True)
    print(json.dumps({'passed': passed, 'total': len(CASES)}))
    if passed != len(CASES):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
