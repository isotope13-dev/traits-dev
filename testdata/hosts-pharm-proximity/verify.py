"""Hosts-file pharming redirect needs same-line proximity.

Run: python3 testdata/hosts-pharm-proximity/verify.py <scratch-directory>

`security-domain-attacker-ip-redirect` pairs a public-IP hosts entry with
a security-domain target. The IP and the name share one hosts line, so the
composite requires them within 256 bytes. Without proximity, a large text
corpus assembles a redirect that was never written: X.509 OID dotted quads
(2.5.4.1) hundreds of kilobytes from an unrelated 360.cn maintainer
address in a database dump.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('objectives/evasion/hosts-file/block-security::'
          'security-domain-attacker-ip-redirect')

POSITIVE = '219.235.3.16\t360safe.com\n'
NEGATIVE = ('2.5.4.1 serialNumber attribute mention here\n'
            + 'filler line\n' * 60
            + 'contact admin at b.360.cn for details\n')


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'same-line-positive.txt': (POSITIVE, True),
        'far-apart-negative.txt': (NEGATIVE, False),
    }
    for name, (body, hostile) in cases.items():
        path = dest / name
        path.write_text(body)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', str(path)],
            env=dict(os.environ, CLEAVE_VALIDATE='0'),
            text=True, capture_output=True, check=True)
        report = json.loads(result.stdout)
        ids = {t['id'] for entry in report['files'] for t in entry['traits']}
        assert (TARGET in ids) == hostile, (name, sorted(ids))
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
