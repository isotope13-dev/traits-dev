#!/usr/bin/env python3
"""Baileys fork archive framing must convict trojanized trees only.

`whatsapp-library-fork-socket-timer-preset-follow` and
`whatsapp-library-fork-forged-viral-forward` pair Baileys library identity
with the file-local timer-follow and forward-forgery hostile traits. A
republished tree carrying both implants must report both wrappers; the same
tree shape without implants must report neither while the identity legs
stay live.

Run `python3 testdata/baileys-fork-archive-framing/check.py <scratch-directory>`.
Minimal npm tarballs are built outside testdata so file-path suppressors
cannot mask the findings under test.
"""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

WRAPPER_NS = 'objectives/supply-chain/trojanized/library/fork-branding'
WRAPPERS = {
    f'{WRAPPER_NS}::whatsapp-library-fork-socket-timer-preset-follow',
    f'{WRAPPER_NS}::whatsapp-library-fork-forged-viral-forward',
}
IDENTITY = {
    'well-known/lib/network/baileys::make-wa-socket-factory',
    'well-known/lib/network/baileys::waproto-namespace',
    'well-known/lib/network/baileys::baileys-library-identity',
}
expected = {
    # Implanted fork: both archive wrappers present.
    'positive.tgz': (WRAPPERS, IDENTITY),
    # Clean fork-shaped tree: identity live, wrappers absent.
    'negative.tgz': (set(), IDENTITY),
    # Unknown root properties are discarded by protobuf; follow remains real.
    'invalid-root.tgz': ({f'{WRAPPER_NS}::whatsapp-library-fork-socket-timer-preset-follow'}, IDENTITY),
}
SOURCES = {
    'positive.tgz': 'positive-socket.js',
    'negative.tgz': 'negative-socket.js',
    'invalid-root.tgz': 'invalid-root-socket.js',
}
PACKAGE_JSON = '{"name": "baileys-fork-fixture", "version": "1.0.0"}\n'

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for archive in sorted(expected):
    target = scratch / archive
    socket_js = (Path(__file__).parent / SOURCES[archive]).read_bytes()
    with tarfile.open(target, 'w:gz') as tar:
        for name, data in (('package/package.json', PACKAGE_JSON.encode()),
                           ('package/lib/socket.js', socket_js)):
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    hostile = set()
    seen = set()
    for entry in report['files']:
        for trait in entry['traits']:
            if trait['crit'] == 5:
                hostile.add(trait['id'])
            seen.add(trait['id'])
    want_hostile, want_legs = expected[archive]
    assert (hostile & WRAPPERS) == want_hostile, (archive, sorted(hostile))
    missing = want_legs - seen
    assert not missing, (archive, sorted(missing))
    print(f'{archive}: passed')
