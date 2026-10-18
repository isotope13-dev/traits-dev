"""Static controls for the three reviewed PE samples; never executes a sample."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import pefile

samples = [Path(p) for p in sys.argv[1:4]]
output = Path(sys.argv[4])
output.mkdir(parents=True, exist_ok=True)
rewrite = 'objectives/impact/infect/binary/rewrite::packed-drive-executable-joiner'
backup = 'objectives/impact/destroy/file-deletion::drive-backup-suffix-deletion'
family = 'well-known/malware/virus/zombie::zombie-packed-file-infector'
clipper = 'objectives/impact/crypto-manipulation/clipboard::go-ethereum-clipboard-overwrite'
persist = 'objectives/persistence/login/registry/run-key::go-clipboard-clipper-run-key-installer'
timing = 'objectives/anti-analysis/timing/evasion::go-shortened-sleep-termination'
debugger = 'objectives/anti-analysis/debugger-detect/check::go-native-debugger-query-branch'
injector = 'well-known/malware/botnet/stormattack::stormattack-service-dll-injector'
cases = []

def add(name, data, required=(), forbidden=()):
    p = output / (name + '.exe')
    p.write_bytes(data)
    cases.append((name, p, set(required), set(forbidden)))

originals = [p.read_bytes() for p in samples]
for i, required in enumerate([(rewrite, backup, family), (injector,), (clipper, persist, timing, debugger)]):
    add('renamed-' + str(i), originals[i], required)
# Same executable and signatures, with a different mapped-section name.
p = pefile.PE(data=originals[0])
b = bytearray(originals[0])
s = p.sections[0]
b[s.get_file_offset():s.get_file_offset()+8] = b'.XPack0\0'
add('alternate-infector-section', b, (rewrite, backup, family))
# Generic references survive; the suffix dispatch and transfer code do not.
b = bytearray(originals[0])
b[0x400:0x400+0x1422] = bytes(0x1422)
add('infector-references-without-code', b, (), (rewrite, backup, family))
# Family labels corroborate behavior instead of being necessary for its verdict.
b = originals[0].replace(b'Zombie.exe', b'xxxxxx.exe').replace(bytes.fromhex('cfebd5d2bbd8cec4bcfe2d5f2d'), b'x'*13)
add('infector-without-family-labels', b, (rewrite, backup), (family,))
# Go pclntab names and literals alone must not establish clipboard tampering.
p = pefile.PE(data=originals[2])
b = bytearray(originals[2])
s = next(s for s in p.sections if s.Name.rstrip(b'\0') == b'.text')
b[s.PointerToRawData:s.PointerToRawData+s.SizeOfRawData] = bytes(s.SizeOfRawData)
add('go-names-without-code', b, (), (clipper, persist, timing, debugger))
# Masked keys tolerate a different transform key without allowing bare names.
b = bytearray(originals[2])
key = p.get_offset_from_rva(0xf698d)
assert b[key:key+3] == bytes.fromhex('83f655')
b[key+2] = 0x44
add('go-alternate-xor-key', b, (clipper, persist))
# Keep legitimate clipboard APIs, but remove the address-selection predicate.
needle = b'^0x[a-fA-F0-9]{40}$'
assert needle in originals[2]
b = originals[2].replace(needle, b'#'*len(needle))
add('go-without-address-predicate', b, (), (clipper, persist))
# Keep the API/name evidence but remove the checked execution sequences.
for name, rva, size, absent in [('timing',0xf7fe5,8,timing),('debugger',0xf6c8f,5,debugger),('clipboard',0xf7e61,5,clipper)]:
    b = bytearray(originals[2]);off = p.get_offset_from_rva(rva)
    b[off:off+size] = b'\x90'*size
    add('go-without-' + name + '-branch', b, (), (absent, persist) if name=='clipboard' else (absent,))

def check(case):
    name, path, required, forbidden = case
    report = output / (name + '.json')
    with report.open('w') as f:
        args = ['cleave','--traits-dir','.', '--format','json']
        if name == 'go-names-without-code':
            # No instructions remain; skip Rizin's pathological empty-function walk.
            args += ['--disable','radare2']
        subprocess.run(args + [str(path)], stdout=f, check=True)
    d = json.loads(report.read_text())
    ids = {t['id'] for f in d['files'] for t in f['traits']}
    assert required <= ids, (name, 'missing', sorted(required-ids))
    assert not (forbidden & ids), (name, 'unexpected', sorted(forbidden&ids))
    return {'case':name,'required':sorted(required),'forbidden':sorted(forbidden),'passed':True}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check,cases))
# A real minimal PE control must not acquire the reviewed behavior claims.
plain = Path('testdata/triage/parser-test-corpus/plain-stub.exe')
results.append(check(('plain-pe-control',plain,set(),{rewrite,backup,family,clipper,persist,timing,debugger,injector})))
Path('testdata/triage/three-pe-first-review/results.json').write_text(json.dumps(results,indent=2)+'\n')
print(str(len(results)) + ' static controls passed')
