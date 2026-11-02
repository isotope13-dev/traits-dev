#!/usr/bin/env python3
"""APK improve controls for precise literals, stream wrappers and job flags."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile
import zlib
from apk_dex_fixture import job_dex


def checksum(blob):
    blob = bytearray(blob)
    blob[12:32] = hashlib.sha1(blob[32:]).digest()
    struct.pack_into('<I', blob, 8, zlib.adler32(blob[12:]) & 0xffffffff)
    return bytes(blob)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cleave', default='../cleave/target/release/cleave')
    ap.add_argument('--samples-root', type=Path, required=True)
    args = ap.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())

    def member(prefix, name):
        paths = [p for p in args.samples_root.rglob('*.apk') if p.name.startswith(prefix)]
        assert len(paths) == 1, (prefix, paths)
        with zipfile.ZipFile(paths[0]) as archive:
            return archive.read(name)

    envelope = 'metadata/file/profile/crypto-envelope::android-asset-cipher-zip-reflection-calls'
    cloud = 'metadata/file/profile/mobile-config::android-sms-text-cloud-config-references'
    persisted = 'micro-behaviors/time/schedule/interval::android-persisted-job-setting'
    query = 'metadata/lang/source/syntax/call/invocation::credential-query-parameter-call-text'
    focus = {envelope, cloud, persisted, query}
    voice = member('2b44a106dc5a', 'classes2.dex')
    qr = member('9228e6cf5457', 'classes2.dex')
    cases = {'asset-cipher-zip.dex': (voice, {envelope}), 'firebase-scan-config.dex': (qr, {cloud})}
    for term, replacement in [
        (b'CipherInputStream', b'DipherInputStream'),
        (b'ZipInputStream', b'YipInputStream'),
        (b'AssetManager', b'ZssetManager'),
        (b'newInstance', b'newInstancf'),
    ]:
        assert len(term) == len(replacement) and term in voice
        cases['without-' + term.decode() + '.dex'] = (checksum(voice.replace(term, replacement)), set())
    for term, replacement in [(b'SMSvsText', b'SMTvsText'), (b'enabled_getting_text_sms', b'enabled_getting_text_smt')]:
        assert len(term) == len(replacement) and term in qr
        cases['without-' + term.decode() + '.dex'] = (checksum(qr.replace(term, replacement)), set())
    for name, value, expected in [('job-true', 1, {persisted}), ('job-false', 0, set()), ('job-reference-only', None, set())]:
        cases[name + '.dex'] = (job_dex(value), expected)
    cases['credential-query.html'] = (b'<script>q.searchParams.set("pin", value);</script>', {query})
    cases['ordinary-query.html'] = (b'<script>q.searchParams.set("timestamp", value);</script>', set())
    cases['plain-string-pool.txt'] = (b'CipherInputStream ZipInputStream AssetManager newInstance setPersisted', set())
    with tempfile.TemporaryDirectory(prefix='apk-improve-controls-') as temporary:
        work = Path(temporary)
        for name, (blob, _) in cases.items():
            (work / name).write_bytes(blob)
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format=json', str(work)],
                                capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr, result.stderr
        seen = set()
        for line in result.stdout.split('\n'):
            if not line.strip():
                continue
            for file in json.loads(line)['files']:
                name = Path(file['path']).name
                actual = {t['id'] for t in file.get('traits', [])} & focus
                assert actual == cases[name][1], (name, actual, cases[name][1])
                assert not [t for t in file.get('traits', []) if t['crit'] == 5], (name, 'unexpected hostile finding')
                seen.add(name)
        assert seen == cases.keys(), (seen, cases.keys())
    print(f'APK improve controls: {len(cases)} passed')


if __name__ == '__main__':
    main()
