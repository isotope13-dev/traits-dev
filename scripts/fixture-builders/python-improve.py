#!/usr/bin/env python3
"""Build static Python review controls. Specimen code is compiled, never run."""
from pathlib import Path
import hashlib
import importlib.util
import json
import lzma
import marshal
import struct
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'scripts/review/python-improve-cases.json'
cases = []


def fixture(label, name, data, required=(), forbidden=(), minimum_hostile=0):
    path = ROOT / 'testdata' / label / 'generated/python-improve' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if len(data) <= 20 * 1024:
        path.with_name(path.name + '.xz').unlink(missing_ok=True)
    if len(data) > 20 * 1024:
        path.unlink(missing_ok=True)
        path = path.with_name(path.name + '.xz')
        data = lzma.compress(data)
    path.write_bytes(data)
    cases.append({'path': str(path.relative_to(ROOT)), 'required': list(required),
                  'forbidden': list(forbidden), 'minimum_hostile': minimum_hostile})
    return path


def pyc(source, filename):
    code = compile(source, filename, 'exec')
    return importlib.util.MAGIC_NUMBER + bytes(12) + marshal.dumps(code)


api = 'micro-behaviors/process/interpreter/python::pyrun-simple-string-flags-reference'
fixture('notable', 'ordinary-pythonrun-declaration.c',
        b'extern int PyRun_SimpleStringFlags(const char *, void *);\n', [api],
        ['well-known/malware/rat/havoc/client-store::pyrun-simplestring-call'])
fixture('hostile', 'havoc-extension-loader.cpp', b'''
extern int PyRun_SimpleStringFlags(const char *, void *);
const char *catalog = "https://raw.githubusercontent.com/p4p1/havoc-store/main/modules.json";
const char *state = "Teamserver.LoadingScript";
const char *download = "wget %1 -O %2";
void load_extension(const char *script) { PyRun_SimpleStringFlags(script, nullptr); }
''', [api, 'well-known/malware/rat/havoc/client-store::havoc-client-store-extension-loader'],
        ['well-known/malware/rat/havoc/client-store::pyrun-simplestring-call'], 1)
old_tasking = 'objectives/command-and-control/backdoor/tasking/http::'
fixture('notable', 'ordinary-command-handlers.pyc', pyc('''
def fetch_command(): return None
def execute_command(command): return command
def command_loop(): return fetch_command()
''', 'ordinary-command-handlers.py'),
        [],
        [old_tasking + n for n in ('fetch-command-name', 'execute-command-name', 'command-loop-name')])
api_ids = ['micro-behaviors/communications/http/server/framework::fastapi-bytecode-api-reference',
           'micro-behaviors/communications/http/server/framework::uvicorn-bytecode-api-reference',
           'micro-behaviors/communications/mcp/client::mcp-stdio-bytecode-api-reference',
           'metadata/lang/source/naming/function/command::execute-tool-bytecode-identifier']
fixture('notable', 'compiled-agent-apis.pyc', pyc('''
import fastapi
import uvicorn
from mcp.client.stdio import stdio_client
from bridge import execute_tool
app = fastapi.FastAPI()
execute_tool("inspect_workspace")
''', 'compiled-agent-apis.py'), api_ids)
fixture('notable', 'quoted-agent-api-names.pyc', pyc('''
examples = ["fastapi", "uvicorn", "mcp.client.stdio", "execute_tool"]
''', 'quoted-agent-api-names.py'), forbidden=api_ids)
fixture('notable', 'unrelated-request-class.pyc', pyc('''
class Request:
    pass
''', 'unrelated-request-class.py'),
        [],
        ['micro-behaviors/communications/http/lib/urllib::request-pyc-name',
         'micro-behaviors/communications/http/lib/urllib::urllib-request-pyc-symbol'])
fixture('notable', 'compiled-subprocess-reference.pyc', pyc('''
import subprocess
subprocess.Popen(["printf", "hello"])
''', 'compiled-subprocess-reference.py'),
        ['micro-behaviors/process/create/subprocess::pyc-subprocess-api-text'],
        ['metadata/binary/code/bytecode::pyc-subprocess-name-reference'])

# Code concealment alone is suspicious, including when it computes only 42.
obfuscated_benign = ("____________=0\nimport pyminifier.obfuscate\n"
                    + "result = eval(compile(eval(compile(" + repr("'40+2'")
                    + ", 'inner', 'eval')), 'outer', 'eval'))\n")
compile(obfuscated_benign, 'obfuscated-benign-calculation.py', 'exec')
fixture('suspicious', 'obfuscated-benign-calculation.py', obfuscated_benign.encode(),
        ['objectives/anti-static/obfuscation/obfuscator/signature::python-obfuscation-suite'])

# Use the existing synthetic runtime, not a specimen native library.
seed_runtime = (ROOT.parent / 'filefacts/testdata/pyarmor/runtime-data.bin').read_bytes()
# Frame the key-material fixture in a valid PE image so native section-scoped
# identity rules exercise the same .data placement as the shipped runtimes.
header = bytearray(512)
header[:2] = b'MZ'
struct.pack_into('<I', header, 0x3c, 0x80)
header[0x80:0x84] = b'PE\0\0'
struct.pack_into('<HHIIIHH', header, 0x84, 0x8664, 1, 0, 0, 0, 240, 0x2022)
struct.pack_into('<H', header, 0x98, 0x20b)
struct.pack_into('<I', header, 0x98 + 8, len(seed_runtime))
struct.pack_into('<Q', header, 0x98 + 24, 0x180000000)
struct.pack_into('<II', header, 0x98 + 32, 4096, 512)
struct.pack_into('<II', header, 0x98 + 56, 8192, 512)
struct.pack_into('<H', header, 0x98 + 68, 3)
struct.pack_into('<I', header, 0x98 + 108, 16)
section_at = 0x188
header[section_at:section_at + 8] = b'.data\0\0\0'
struct.pack_into('<IIII', header, section_at + 8, len(seed_runtime), 4096, len(seed_runtime), 512)
struct.pack_into('<I', header, section_at + 36, 0xc0000040)
runtime = bytearray(header + seed_runtime)
runtime[512:514] = b'\0\0'  # the seed's old mock image is not a second PE
runtime = bytes(runtime)
id_at = runtime.index(b'pyarmor-vax-')
u32 = lambda b, off: struct.unpack_from('<I', b, off)[0]
base = id_at + 0x34
public_at = base + u32(runtime, id_at + 0x24)
public_len = u32(runtime, id_at + 0x28)
license_at = base + u32(runtime, id_at + 0x2c)
extra_len = u32(runtime, license_at + 4)
salt = bytes(b ^ 0xf1 for b in runtime[0x500:0x500 + 270])
key = hashlib.md5(runtime[id_at:id_at + 20] + runtime[public_at:public_at + public_len]
                  + runtime[license_at + 32:license_at + 32 + extra_len] + salt).digest()


def protected_wrapper(bytecode):
    flags = 0x40912
    body = bytecode[16:]
    plain = struct.pack('<IIIII', 32, 0, len(body), flags, 8) + bytes(12) + body
    outer = bytearray(64)
    outer[:8] = b'PY314159'
    outer[9:11] = bytes([3, 14])
    outer[12:16] = bytecode[:4]
    struct.pack_into('<III', outer, 0x1c, 64, len(plain), flags)
    outer[0x2c:0x34] = b'fixture!'
    nonce = struct.pack('<I', flags) + outer[0x2c:0x34]
    cipher = subprocess.run(['openssl', 'enc', '-aes-128-ctr', '-K', key.hex(),
                             '-iv', (nonce + b'\0\0\0\2').hex()], input=plain,
                            capture_output=True, check=True).stdout
    blob = bytes(outer) + cipher
    return ("from pyarmor_runtime_314159 import __pyarmor__\n"
            f"__pyarmor__(__name__, __file__, {blob!r})\n").encode()


def protected_zip(label, name, bytecode, required=(), minimum_hostile=0, reverse=False):
    import io
    out = io.BytesIO()
    entries = [('arbitrarily-renamed.py', protected_wrapper(bytecode)),
               ('companion.bin', runtime)]
    if reverse:
        entries.reverse()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name_in_zip, data in entries:
            info = zipfile.ZipInfo(name_in_zip, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    return fixture(label, name, out.getvalue(), required=required,
                   minimum_hostile=minimum_hostile)


# Protected benign output keeps the real protection finding, and exposes APIs.
protected_zip('suspicious', 'protected-agent-apis.zip',
              (ROOT / 'testdata/notable/generated/python-improve/compiled-agent-apis.pyc').read_bytes(),
              required=['well-known/lib/runtime/scripted/pyarmor::native-runtime-marker', *api_ids])
# An established attack PYC must retain its hostile findings behind protection.
attack = (ROOT / 'testdata/hostile/generated/whl-bad-triage-20261028/audit-registry-egress.pyc').read_bytes()
protected_zip('hostile', 'protected-audit-registry-egress.zip', attack,
              required=['well-known/lib/runtime/scripted/pyarmor::native-runtime-marker'],
              minimum_hostile=1, reverse=True)
MANIFEST.write_text(json.dumps({'cases': cases}, indent=2) + '\n')
print(f'Built {len(cases)} non-executed fixtures')
