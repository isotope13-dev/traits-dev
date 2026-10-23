"""Static controls for relocated observations and native byte scrambling.
Generate only inert PE files; never execute them. Pass a scratch directory.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
pe_image = runpy.run_path(str(ROOT/'testdata/native-rat-loader-triage/verify.py'))['pe_image']
XOR = 'micro-behaviors/data/encoding/xor::'
FLAT = 'objectives/anti-static/obfuscation/encoding/buffer::flattened-xorshift-byte-scrambling'
CROC = 'well-known/dual-use/transfer/croc::croc-cli-implementation'
TUN = 'micro-behaviors/network/tunnel::userspace-networking-reference'
HUJSON = 'metadata/import/package::tailscale-hujson-module-reference'
AGENTICS = 'well-known/dual-use/tunnel/agentics-companion::agentics-tailscale-companion'


def main():
    dest = Path(sys.argv[1]); dest.mkdir(parents=True, exist_ok=True)
    state = bytes.fromhex('4C89D0 48C1E00D 4C31D0 488BF8 48C1EF07 8D8D01020304 4833F8 4C8BD7 49D3E2 4931FA 48BF1122334455667788 490FAFFA')
    xor = bytes.fromhex('C1E103 4C89C3 48D3EB 301E')
    branch = bytes.fromhex('65488B0C2558000000 480F44C8 486301 4801E8 FFE0')
    code = b'\xc3'+branch*5+state+xor
    atoms = {XOR+'x64-xorshift-multiply-state-update', XOR+'x64-shift-selected-byte-xor'}
    hujson = b'github.com/tailscale/hujson\0'
    cases = [
      ('flattened-xor.exe', pe_image(code=code), atoms|{FLAT}, set()),
      ('ordinary-xor.exe', pe_image(code=b'\xc3'+state+xor), atoms, {FLAT}),
      ('prng-only.exe', pe_image(code=b'\xc3'+branch*5+state), {XOR+'x64-xorshift-multiply-state-update'}, {FLAT,XOR+'x64-shift-selected-byte-xor'}),
      ('data-only.exe', pe_image(code=b'\xc3'+branch*5,data=state+xor), set(), atoms|{FLAT}),
      ('missing-write.exe', pe_image(code=code[:-2]+b'\x90\x90'), {XOR+'x64-xorshift-multiply-state-update'}, {FLAT,XOR+'x64-shift-selected-byte-xor'}),
      ('croc-cli.exe', pe_image(data=b'github.com/schollz/croc/v11/src/cli.RunContext\0'), {CROC},set()),
      ('croc-url.exe', pe_image(data=b'https://github.com/schollz/croc\0'), set(),{CROC}),
      ('hujson-library.exe', pe_image(data=hujson,overlay=b'\0'*1048576), {HUJSON},{AGENTICS}),
      ('agentics.exe', pe_image(data=hujson+b'agentics.co.za/router/main\0',overlay=b'\0'*1048576), {HUJSON,AGENTICS},set()),
      ('userspace.go', b'package main\nvar tun = "userspace-networking"\n', {TUN},set()),
      ('ordinary.go', b'package main\nvar tun = "kernel-networking"\n',set(),{TUN}),
      ('emit.cs', b'using System.Reflection.Emit; class Example { void Build(ILGenerator il) { il.Emit(OpCodes.Ret); } }', {'micro-behaviors/metaprogramming/generation::dotnet-named-opcode-emission'},set()),
      ('il-preprocessor.cs', b'using System.Reflection.Emit; class Builder { void Build(ILGenerator il) { string ops = "lodstra|lodstrw"; il.Emit(OpCodes.Ret); } }', {'micro-behaviors/metaprogramming/generation::dotnet-named-opcode-emission', 'objectives/anti-static/obfuscation/instruction/insertion-junk::csharp-assembly-string-loader-preprocessor'},set()),
      ('event.cs', b'class Example { void Run() { emitter.Emit(1); } }', set(),{'micro-behaviors/metaprogramming/generation::dotnet-named-opcode-emission'}),
    ]
    engine=os.environ.get('CLEAVE','cleave')
    def check(case):
        name,data,required,forbidden=case;p=dest/name;p.write_bytes(data)
        proc=subprocess.run([engine,'--traits-dir',str(ROOT),'--format','json',str(p)],capture_output=True,check=True,env={**os.environ,'CLEAVE_VALIDATE':'0'})
        j=json.loads(proc.stdout);ids={t['id'] for f in j['files'] for t in f.get('traits',[])}
        assert required <= ids,(name,'missing',required-ids)
        assert not forbidden & ids,(name,'unexpected',forbidden & ids)
        return {'name':name,'required':sorted(required),'forbidden':sorted(forbidden),'passed':True}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        results=list(ex.map(check,cases))
    (dest/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    for r in results:print('PASS',r['name'])


if __name__=='__main__':main()
