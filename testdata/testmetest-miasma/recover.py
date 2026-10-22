"""Statically recover the pinned sample; never execute its JavaScript or scripts.

python3 recover.py SAMPLE.tgz OUTPUT_DIRECTORY
Requires Python 3 and Node.js with their standard libraries only.
"""
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

SHA256 = '32dd68c748eefd03a25b7104b648685b877672581c94741099899d789701c6de'
HERE = Path(__file__).resolve().parent


def recover(sample, dest):
    assert hashlib.sha256(sample.read_bytes()).hexdigest() == SHA256, 'wrong sample'
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'package').mkdir(exist_ok=True)
    # Extract exactly the expected regular files, with no archive-controlled paths.
    with tarfile.open(sample) as archive:
        for name in ['index.js', 'lib_native.dat', 'package.json', 'binding.gyp', 'README.md']:
            member = archive.getmember('package/' + name)
            assert member.isfile() and member.size < 2_000_000
            (dest / 'package' / name).write_bytes(archive.extractfile(member).read())
    source = (dest / 'package/index.js').read_text()
    numbers = re.search(r'\[([\d,]+)\]', source)[1]
    stage = ''.join(chr(int(n)) for n in numbers.split(','))
    stage = re.sub('[a-zA-Z]', lambda m: chr((ord(m[0]) - (65 if m[0].isupper() else 97) + 1) % 26 + (65 if m[0].isupper() else 97)), stage)
    (dest / 'stage1.js').write_text(stage)
    subprocess.run(['node', str(HERE / 'decrypt-stages.cjs'), str(dest)], check=True)

    source = (dest / 'payload.js').read_text()
    table = re.search(r'function _0x28e1\(\)\{const _0x331bb2=\[(.*?)\];', source)[1]
    encoded = re.findall("'([^']*)'", table)
    assert len(encoded) == 4004
    translation = str.maketrans('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    values = [base64.b64decode(s.translate(translation) + '=' * (-len(s) % 4)).decode() for s in encoded]
    # Rotation is verified against the decoder's arithmetic guard, not executed.
    def number(rotation, index):
        value = values[(index - 0x1ad + rotation) % len(values)]
        return int(re.match(r'^[+-]?\d+', value)[0])
    rotations = []
    for rotation in range(len(values)):
        try:
            v = lambda i: number(rotation, i)
            total = -v(0x1061) * v(0xe57)/2 - v(0x7bc)/3 * v(0x45a)/4 + v(0xcc3)/5 * v(0x83a)/6 - v(0x71c)/7 * -v(0x75c)/8 + v(0x776)/9 * -v(0xb29)/10 - v(0xcc9)/11 + v(0x3a6)/12
            if total == 0xd8044:
                rotations.append(rotation)
        except (TypeError, ValueError):
            pass
    assert rotations == [123], rotations
    aliases = {'_0x53a9'}
    assignments = re.findall(r'\b(_0x[\da-f]+)=(_0x[\da-f]+)\b', source)
    while True:
        before = len(aliases)
        aliases.update(lhs for lhs, rhs in assignments if rhs in aliases)
        if before == len(aliases):
            break
    constants = {}
    for match in re.finditer(r'\b(_0x[\da-f]+)=\{([^{}]*)\}', source):
        for key, value in re.findall(r'(_0x[\da-f]+):(0x[\da-f]+|\d+)', match[2]):
            constants[match[1] + '.' + key] = int(value, 0)
    count = 0
    def replace(match):
        nonlocal count
        if match[1] not in aliases:
            return match[0]
        arg = match[2]
        index = constants.get(arg) if '.' in arg else int(arg, 0)
        if index is None:
            return match[0]
        count += 1
        return json.dumps(values[(index - 0x1ad + 123) % len(values)])
    source = re.sub(r'\b(_0x[\da-f]+)\((0x[\da-f]+|\d+|_0x[\da-f]+\._0x[\da-f]+)\)', replace, source)
    assert count == 15445, count
    (dest / 'payload-decoded.js').write_text(source)
    subprocess.run(['node', str(HERE / 'decrypt-strings.cjs'), str(dest)], check=True)
    manifest = json.loads((HERE / 'functions.json').read_text())
    clear = (dest / 'payload-clear.js').read_bytes()
    assert hashlib.sha256(clear).hexdigest() == manifest['payload_sha256']

    # Correct suffixes matter: .github-actions alone isn't recognized as a workflow.
    types = {'M5': '.yml', '_5': '.yml', 'Yc': '.yaml', 'Vc': '.yaml',
             'Kt': '.py', 'D5': '.py', 'Ti': '.js', 'xi': '.json', 'qc': '.pem',
             'es': '.sh', 'ts': '.py', 'Zc': '.sh', 'Qc': '.sh', 'Xc': '.py',
             'el': '.json', 'vr': '.pem'}
    recovered = dest / 'recovered'
    (recovered / '.github/workflows').mkdir(parents=True, exist_ok=True)
    shutil.copyfile(dest / 'payload-clear.js', recovered / 'payload.js')
    # Parser-derived top-level boundaries, pinned by source and slice hashes.
    # Small units avoid the full bundle's flow budget and output finding cap.
    (recovered / 'functions').mkdir(exist_ok=True)
    utf16 = clear.decode().encode('utf-16-le')
    for row in manifest['functions']:
        fragment = utf16[row['start'] * 2:row['end'] * 2].decode('utf-16-le').encode()
        assert hashlib.sha256(fragment).hexdigest() == row['sha256']
        (recovered / 'functions' / row['file']).write_bytes(fragment)
    resources = {row['name']: row for row in json.loads((dest / 'embedded/index.json').read_text())}
    assert set(resources) == set(types)
    for name, suffix in types.items():
        target = recovered / ('.github/workflows' if name in ['M5', '_5'] else '') / (name + suffix)
        shutil.copyfile(dest / 'embedded' / resources[name]['filename'], target)
    with tarfile.open(dest / 'recovered.tar', 'w') as archive:
        archive.add(recovered, arcname='recovered')
    print('Recovered:', recovered, '(analysis material; do not execute)')


if __name__ == '__main__':
    recover(Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).resolve())
