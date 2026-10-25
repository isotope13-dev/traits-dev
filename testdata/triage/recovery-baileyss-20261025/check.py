#!/usr/bin/env python3
"""Static rule checks; copy controls outside testdata to avoid fixture downgrades."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
OFFICIAL = 'objectives/impact/ui/manipulation/social::forged-official-whatsapp-newsletter-attribution'
VIRAL = 'objectives/impact/ui/manipulation/social::forged-viral-whatsapp-forward'
FIXED = 'micro-behaviors/communications/messaging/channel::fixed-whatsapp-newsletter-message-attribution'
EXEC = 'micro-behaviors/process/create/shell/local::node-exec-command-variable'
DIR = 'micro-behaviors/fs/directory/readdir::cpp-filesystem-directory-iterator'
UNLOAD = 'micro-behaviors/os/registry/hive::regunloadkey-call-source'
cases = []
def add(name, source, yes=(), no=()):
    target = OUT / name
    target.write_text(source)
    cases.append((target, set(yes), set(no)))

for name in ['official-contextinfo.js', 'official-root-nearmiss.js', 'caller-channel-contextinfo.js']:
    add(name, (HERE / name).read_text(),
        [OFFICIAL, VIRAL, FIXED] if name == 'official-contextinfo.js' else [FIXED],
        [] if name == 'official-contextinfo.js' else [OFFICIAL, VIRAL])
add('renamed-assignment.js', '''
message.imageMessage.contextInfo.forwardedNewsletterMessageInfo = {
 newsletterName: 'WhatsApp', newsletterJid: '100000000000001@newsletter'
}; relayMessage(jid, message, {});''', [OFFICIAL], [VIRAL])
add('wrong-context.js', (HERE / 'official-contextinfo.js').read_text().replace('contextInfo', 'messageContextInfo'), [FIXED], [OFFICIAL, VIRAL])
add('invalid-channel.js', (HERE / 'official-contextinfo.js').read_text().replace('100000000000001@newsletter', '0@newsletter'), [], [OFFICIAL, VIRAL])
add('distant-exec.js', "import { exec } from 'child_process';\n" + '\n' * 85 + 'function thumb(cmd) { exec(cmd, err => {}); }\n', [EXEC])
add('unbound-exec.js', 'function thumb(cmd) { exec(cmd); }\n', [], [EXEC])
add('import-only.js', "import { exec } from 'child_process';\n", [], [EXEC])
add('native-operations.cpp', '''
#include <windows.h>
void cleanup() { RegUnLoadKeyW(HKEY_USERS, L"Mounted"); }
void list() { auto items = std::filesystem::directory_iterator(path); }
''', [DIR, UNLOAD])
add('different-native-operations.cpp', '''
void list() { auto items = std::filesystem::recursive_directory_iterator(path); }
void label() { const char *name = "RegUnLoadKeyW"; }
''', [], [DIR, UNLOAD])

r = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                    '--format', 'json', str(OUT)], capture_output=True, text=True,
                   env=dict(os.environ, CLEAVE_VALIDATE='0'), check=True)
reports = {}
remaining = r.stdout.lstrip()
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    for f in report['files']:
        reports[Path(f['path']).name] = f.get('traits', [])
    remaining = remaining[end:].lstrip()
results = []
for target, yes, no in cases:
    ts = reports[target.name]
    seen = {t['id']: t['crit'] for t in ts}
    missing = sorted(yes - seen.keys())
    unexpected = sorted(no & seen.keys())
    results.append(dict(file=target.name, missing=missing, unexpected=unexpected,
                        hostile=[t['id'] for t in ts if t['crit'] == 5]))
    assert not missing and not unexpected, results[-1]
    if OFFICIAL in yes: assert seen[OFFICIAL] == 5
    if VIRAL in yes: assert seen[VIRAL] == 5
(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(f'{len(cases)} static controls passed')
