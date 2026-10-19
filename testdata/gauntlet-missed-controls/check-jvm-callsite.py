"""Non-executed class-format controls for the XOR/callsite observation.

These are static parser/matcher fixtures, not a runnable malware or decrypter.
CP references and Code bytes are generated as data; no JVM is started.
"""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', required=True)
parser.add_argument('--sample', type=Path, help='Optional external resolver class')
parser.add_argument('--jar-regression', action='store_true')
parser.add_argument('--jar-only', action='store_true')
parser.add_argument('--reports', type=Path)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[2]
finding = 'objectives/anti-static/obfuscation/reflection/invoke::jvm-shifted-xor-callsite-resolver'
names = ['java/lang/invoke/MutableCallSite', 'fromMethodDescriptorString',
         'setTarget', 'java/lang/StringBuilder']
xor_loop = bytes.fromhex('03 2c 5f 5a b6 00 01 1b 10 10 7c 82 '
                        '2c 5d 58 5b 57 5b 57 5f 5b 5f b6 00 02 '
                        '04 60 59 2c b6 00 03 a1 ff df')
member = bytes.fromhex('15 06 15 05 b8 00 04 12 05 b6 00 06 '
                      '3a 08 19 08 03 32 b8 00 07 3a 09')


def class_bytes(markers, code):
    pool = []
    def utf8(value):
        data = value.encode()
        pool.append(b'\x01' + struct.pack('>H', len(data)) + data)
        return len(pool)
    def klass(value):
        index = utf8(value)
        pool.append(b'\x07' + struct.pack('>H', index))
        return len(pool)
    this = klass('ObservationControl')
    parent = klass('java/lang/Object')
    method = utf8('observe')
    desc = utf8('()V')
    attribute = utf8('Code')
    for marker in markers:
        utf8(marker)
    payload = struct.pack('>HHI', 8, 12, len(code)) + code + bytes(4)
    # Attribute name is u16; keep length a separate u32.
    methods = struct.pack('>HHHHH', 1, 9, method, desc, 1) + struct.pack('>HI', attribute, len(payload)) + payload
    return (bytes.fromhex('cafebabe00000034') + struct.pack('>H', len(pool)+1) + b''.join(pool)
            + struct.pack('>HHHHH', 0x21, this, parent, 0, 0) + methods + bytes(2))


env = dict(os.environ, CLEAVE_NO_UPDATE_CHECK='1', XDG_CACHE_HOME='/tmp/gauntlet-cache',
           RAYON_NUM_THREADS='2')
def analyze(path, memory=100, label=None):
    run = subprocess.run([args.cleave, '--traits-dir', str(repo), '--max-file-mem', str(memory),
                          '--format=json', 'analyze', str(path)],
                         env=env, check=True, capture_output=True, text=True, timeout=120)
    report = json.loads(run.stdout)
    if label and args.reports:
        args.reports.mkdir(parents=True, exist_ok=True)
        (args.reports/(label+'.json')).write_text(run.stdout)
    return {t['id']:t for f in report['files'] for t in f.get('traits', [])}


cases = [('both-layouts', names, xor_loop+member+b'\xb1', True),
         ('names-only', names, b'\xb1', False),
         ('xor-only', names, xor_loop+b'\xb1', False),
         ('resolver-only', names, member+b'\xb1', False),
         ('no-xor-operation', names, xor_loop.replace(b'\x7c\x82', b'\x7c\x80')+member+b'\xb1', False),
         ('no-shift', names, xor_loop.replace(b'\x10\x10\x7c', b'\x10\x10\x78')+member+b'\xb1', False),
         ('forward-backedge', names, xor_loop[:-2]+b'\x00\x1f'+member+b'\xb1', False)]
cases += [('without-'+str(index), [n for n in names if n!=name], xor_loop+member+b'\xb1', False)
          for index, name in enumerate(names)]
if args.jar_only:
    cases = []
with tempfile.TemporaryDirectory(prefix='gauntlet-callsite-') as scratch:
    for label, markers, code, want in cases:
        path = Path(scratch)/(label+'.class')
        path.write_bytes(class_bytes(markers, code))
        traits = analyze(path)
        assert (finding in traits)==want, label
        assert not any(t['crit']==5 for t in traits.values()), label
        print('PASS', label, flush=True)
    if args.jar_regression or args.jar_only:
        archive = Path(scratch)/'selection.jar'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_STORED) as jar:
            # More than twenty higher-salience decoys push the resolver out
            # of the normal ranked sample. No specimen code is executed.
            decoy = class_bytes(['java/lang/ProcessBuilder', 'java/net/HttpURLConnection'], b'\xb1')
            for index in range(25):
                jar.writestr('padding/Decoy'+str(index)+'.class', decoy)
            jar.writestr('resolver/Hidden.class', class_bytes(names, xor_loop+member+b'\xb1'))
            # The stored padding crosses the 1 MiB disk-path threshold.
            jar.writestr('META-INF/padding.bin', bytes(1100000))
        for memory in (100, 1):
            traits = analyze(archive, memory, 'inline-jar-memory-'+str(memory))
            assert finding in traits, ('JAR selector', memory)
            print('PASS inline-YARA JAR selection, max-file-mem='+str(memory), flush=True)
if args.sample:
    traits = analyze(args.sample)
    assert finding in traits, 'real resolver class must match'
    assert traits[finding]['crit']==4
    print('PASS external resolver class', flush=True)
