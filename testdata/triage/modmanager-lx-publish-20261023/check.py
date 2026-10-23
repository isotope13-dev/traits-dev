"""Inert controls for observed GTA/Sciter name collisions and install publishing."""
import concurrent.futures
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CLEAVE = os.environ.get('CLEAVE', 'cleave')
PE = runpy.run_path(str(ROOT / 'testdata/first-reasoned-native-review/check.py'))['pe64']
AGENT = 'micro-behaviors/data/llm/agent::native-ai-agent-identity'
CADDY = 'micro-behaviors/communications/http/server/listener::caddy-server-command'
ATOP = 'micro-behaviors/os/sysinfo/performance::atop-tool'
HEADER = 'metadata/lang/source/declaration::long-function-or-sub-header'
KEY = 'objectives/anti-static/obfuscation/string/reconstruct::wscript-inline-xor-method-key'
PUBLISH = 'objectives/impact/spam::install-hook-temp-manifest-and-publish'

def main():
    dest = Path(sys.argv[1]); dest.mkdir(parents=True, exist_ok=True)
    cases = []
    def pe(name, data, required=(), absent=()):
        cases.append((name + '.exe', PE(data=data), set(required), set(absent)))
    pe('gta-character-and-vehicle', b'claude\0Claude (id299)\0claude-id299\0caddy.png\0', absent=[AGENT, CADDY])
    pe('wide-gta-names', 'CLAUDE.PNG\0caddy.png\0'.encode('utf-16le'), absent=[AGENT, CADDY])
    pe('sciter-compositing', b'blend-atop\0', absent=[ATOP])
    pe('atop-inventory', b'atop\0', required=[ATOP])
    pe('atop-command', b'/usr/bin/atop -w capture.raw\0', required=[ATOP])
    for name in ['claude.exe', 'claudecode', 'claude-code', 'kiro-cli', 'kiro.exe', 'cursor-agent']:
        pe('agent-' + name.replace('.', '-'), name.encode() + b'\0', required=[AGENT])
    pe('wide-cli', 'claude.exe\0'.encode('utf-16le'), required=[AGENT])
    pe('caddy-launch', b'caddy.exe run --config Caddyfile\0', required=[CADDY])
    pe('caddy-start', b'caddy start\0', required=[CADDY])
    pe('tiscript-header', b'function getInstallPath()\n{\nreturn 0;\n}\n', required=[HEADER])
    pe('vb-header', b'Function ExecutePayload()\nEnd Function\n', required=[HEADER, 'metadata/lang/source/shape::embedded-vb-long-procedure-block'])
    # Preserve the live AI-agent attack consumers with explicit CLI spellings.
    data = b'claude.exe\0proxy_ca\0intercepting https\0custom upstream\0register-guest\0https://service.top\0'
    pe('agent-attack-consumers', data, required=[AGENT, 'objectives/collection/network/ssl-intercept::ai-agent-https-proxy-intercept', 'objectives/supply-chain/trojanized/app/ai-agent-tools::trojanized-native-ai-agent-control-plane'])
    body = "(function(){var s='Abc';var o='';for(var i=0;i<s.length;i++)o+=String.fromCharCode(s.charCodeAt(i)^2);return o;})()"
    cases.append(('decoded-key.js', ('WScript[' + body + ']("argument");').encode(), {KEY}, set()))
    cases.append(('plain-key.js', b'WScript[(function(){return "Echo";})()]("hello");', set(), {KEY}))
    cases.append(('unrelated-decoder.js', ('var value=' + body + '; WScript[(function(){return "Echo";})()](value);').encode(), set(), {KEY}))
    cases.append(('quoted-decoder.js', ('var example=' + json.dumps('WScript[' + body + ']("argument");') + ';').encode(), set(), {KEY}))
    cases.append(('real-mask.c', b'unsigned low_bit(unsigned value) { return value & 1; }\n', {'micro-behaviors/data/arithmetic::low-bit-mask-expression'}, set()))
    cases.append(('mask-text.c', b'const char *text="value & 1";\n', set(), {'micro-behaviors/data/arithmetic::low-bit-mask-expression'}))
    cases.append(('lowbit-only.php', b'<?php return $value & 1;\n', {'metadata/lang/source/syntax/operator::low-bit-mask-expression-text'}, {'metadata/lang/source/shape::source-syntax-known-benign-context'}))
    for name, scripts, required in [
        ('direct', {'postinstall': 'd=$(mktemp -d); printf "{}" > $d/package.json; npm publish $d; rm -rf $d'}, {PUBLISH}),
        ('release', {'release': 'd=$(mktemp -d); printf "{}" > $d/package.json; npm publish $d'}, set()),
        ('temporary-build', {'postinstall': 'd=$(mktemp -d); printf "{}" > $d/package.json; node build.js'}, set()),
    ]:
        content=json.dumps({'name':'control','version':'1.0.0','scripts':scripts}).encode()
        cases.append((name+'/package.json',content,required,set() if required else {PUBLISH}))
    def run(case):
        name, data, required, absent = case
        path=dest/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        result=subprocess.run([CLEAVE,'--traits-dir',str(ROOT),'--format','json',str(path)],capture_output=True,text=True,check=True)
        report=json.loads(result.stdout); ids={t['id'] for f in report['files'] for t in f.get('traits',[])}
        assert required <= ids, (name,'missing',required-ids)
        assert not absent & ids, (name,'unexpected',absent & ids)
        return {'case':name,'passed':True}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(run,cases))
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
