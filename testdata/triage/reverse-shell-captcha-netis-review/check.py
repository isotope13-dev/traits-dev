#!/usr/bin/env python3
"""Check retained attacks and corrected generic HTTP/WebCrypto observations."""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OLD_CRYPTO = 'micro-behaviors/crypto/symmetric/decrypt::webcrypto-obfuscated-decrypt-call'
NEW_CRYPTO = 'micro-behaviors/crypto/decrypt::webcrypto-decrypt-source-call'
OLD_POST = 'well-known/malware/botnet/mirai/lzrd::lzrd-cdn-cgi-post-fragment'
NEW_POST = 'micro-behaviors/communications/http/message::cdn-cgi-request-template-with-header-delimiter'
LZRD = 'well-known/malware/botnet/mirai/lzrd::lzrd-http-ddos-profile'
EXPIRY = 'objectives/credential-access/phishing/landing::obfuscated-turnstile-expiry-decrypt-redirect'


def elf32(code):
    """Inert ELF32 section fixture: no program headers or executable entry."""
    names = b'\0.text\0.shstrtab\0'
    data = bytearray(52)
    code_off = len(data)
    data += code
    name_off = len(data)
    data += names
    data += bytes(-len(data) % 4)
    shoff = len(data)
    data += bytes(40)
    data += struct.pack('<IIIIIIIIII', 1, 1, 6, 0x8048000 + code_off, code_off,
                        len(code), 0, 0, 1, 0)
    data += struct.pack('<IIIIIIIIII', 7, 3, 0, 0, name_off, len(names), 0, 0, 1, 0)
    struct.pack_into('<16sHHIIIIIHHHHHH', data, 0,
                     b'\x7fELF\x01\x01\x01' + bytes(9), 2, 3, 1,
                     0, 0, shoff, 0, 52, 0, 0, 40, 3, 2)
    return bytes(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--traits-dir', type=Path, default=ROOT)
    ap.add_argument('--baseline', action='store_true')
    ap.add_argument('--record', type=Path)
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location('elf_controls', ROOT / 'testdata/triage/mirai-first-review/check.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    crypto = OLD_CRYPTO if args.baseline else NEW_CRYPTO
    post = OLD_POST if args.baseline else NEW_POST
    cases = []

    def case(name, data, yes=(), no=()):
        cases.append((name, data, set(yes), set(no)))

    fixture = ROOT / 'testdata/triage/turnstile-redirect'
    case('decrypt-attack.html', (fixture / 'failure-redirect.html').read_bytes(), [crypto, EXPIRY])
    case('dot-decrypt-attack.html', (ROOT / 'testdata/triage/version-drift-decocms/turnstile-failure-redirect.html').read_bytes(), [crypto, EXPIRY])
    case('existing-benign.html', (fixture / 'benign.html').read_bytes(),
         [], [crypto])
    failure = (fixture / 'failure-redirect.html').read_bytes()
    for method in (b'encrypt', b'digest', b'importKey'):
        case(method.decode() + '-near-miss.html', failure.replace(b"['decrypt']", b"['" + method + b"']"),
             [crypto, EXPIRY] if args.baseline else [], [] if args.baseline else [crypto, EXPIRY])
    case('computed-method.js', b"crypto['subtle'][operation](input);", ['micro-behaviors/crypto/symmetric/decrypt::webcrypto-subtle-bracket-obfuscated-call'] if args.baseline else
         ['micro-behaviors/data/control-flow/dispatch::js-computed-property-call'],
         [] if args.baseline else [crypto])
    for name, text in [('ordinary-post', b'POST /cdn-cgi/test HTTP/1.1\0'),
                       ('ordinary-post-header', b'POST /cdn-cgi/test HTTP/1.1\r\nX-Test: value\0')]:
        case(name + '.elf', mod.elf(text + bytes(512)), [post] if name.endswith('header') else [],
             [LZRD] + ([] if args.baseline else [OLD_POST]))
    brand = bytes(x ^ 0x22 for x in b'lzrd cock fest\0')
    case('lzrd-family-positive.elf', mod.elf(brand + b'\0POST /cdn-cgi/test HTTP/1.1\r\nX-Test: value\0/proc/net/tcp\0' + bytes(512)), [post, LZRD])
    banners = b'Server: DOSarrest\0Server: cloudflare-nginx\0'
    case('plain-banners.elf', mod.elf(banners),
         [('objectives/impact/dos/http::' if args.baseline else 'micro-behaviors/communications/http/fingerprint::') + 'dosarrest-server-banner'])
    # Use the real encoded pool so the decoder's table heuristics are exercised.
    sample = Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-9cd2ba5d/samples/749e4e8f58d8/176.65.139.232_sample.bin')
    if sample.exists():
        case('xor-banners.elf', sample.read_bytes(),
             [('objectives/impact/dos/http::' if args.baseline else 'micro-behaviors/communications/http/fingerprint::') + 'dosarrest-server-banner-xor'])

    if not args.baseline:
        for syscall, number, trait in [
            ('unlink', '0A', 'micro-behaviors/fs/delete/file/syscall::i386-unlink-syscall-stub'),
            ('prctl', 'AC', 'micro-behaviors/process/control/prctl::i386-prctl-syscall-stub'),
        ]:
            stub = bytes.fromhex('53 89 FB B8 ' + number + ' 00 00 00 CD 80 5B C3')
            case(syscall + '-stub.elf', elf32(stub), [trait])
            # Adjacent syscall numbers and the same bytes in another ISA are controls.
            other = bytearray(stub)
            other[4] += 1
            case(syscall + '-different-syscall.elf', elf32(other), no=[trait])
            case(syscall + '-wrong-architecture.elf', mod.elf(code=stub), no=[trait])


    with tempfile.TemporaryDirectory(prefix='fallout-controls-') as tmp:
        paths = []
        for name, data, _, _ in cases:
            path = Path(tmp) / name
            path.write_bytes(data)
            paths.append(str(path))
        result = subprocess.run(['cleave', '--no-update-check', '--traits-dir', str(args.traits_dir),
                                 '--disable', 'radare2,upx,third-party', '--format', 'json', 'analyze', *paths],
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        reports = {}
        output = result.stdout
        decoder = json.JSONDecoder()
        while output.strip():
            report, end = decoder.raw_decode(output.lstrip())
            reports.update({Path(f['path']).name: f for f in report['files']})
            output = output.lstrip()[end:]
        for name, _, yes, no in cases:
            ids = {t['id'] for t in reports[name]['traits']}
            assert yes <= ids, (name, 'missing', sorted(yes - ids))
            assert not no & ids, (name, 'unexpected', sorted(no & ids))
            print('PASS', name)
        if args.record:
            args.record.write_text(json.dumps(reports, indent=2))
    print(f'{len(cases)} controls passed')


if __name__ == '__main__':
    main()
