"""Verify positive, changed-key, operation-only and distant-evidence controls."""
import json,sys
from pathlib import Path
report=Path(sys.argv[1])
files={}
for line in report.read_text().split('\n'):
    if not line:continue
    item=json.loads(line)
    for f in item['raw']['files']:
        files[Path(f['path']).name]={t['id'] for t in f['traits']}
xor='micro-behaviors/data/decode/xor::x64-position-rotated-key-byte-decoder'
exp='micro-behaviors/os/api-resolution/manual::x64-pe-signature-export-rva-read'
conceal='objectives/anti-static/obfuscation/imports/runtime-concealment::rotating-key-decoder-near-export-parser'
platform='micro-behaviors/os/sysinfo/platform/runtime::node-os-named-platform-call'
release='micro-behaviors/os/sysinfo/platform/runtime::node-os-named-release-call'
gzip='micro-behaviors/data/compress/gzip::node-promisify-gzip'
telemetry='micro-behaviors/os/telemetry/activity::posthog-telemetry-client'
server='micro-behaviors/communications/http/server/framework::server-express'
checks={
 'rotating-exports.exe':({xor,exp,conceal},set()),
 'xor-only.exe':({xor},{exp,conceal}),
 'export-only.exe':({exp},{xor,conceal}),
 'wrong-directory.exe':({xor},{exp,conceal}),
 'no-xor.exe':({exp},{xor,conceal}),
 'distant.exe':({xor,exp},{conceal}),
 'label-only.exe':({'metadata/binary/section/label::enigma-numbered-section-label'},{conceal}),
 'node-positive.ts':({platform,release,gzip},set()),
 'node-comments.ts':(set(),{platform,release,gzip}),
 'node-names-only.ts':(set(),{platform,release,gzip}),
 'node-imports-only.ts':(set(),{platform,release,gzip}),
 'posthog-client.ts':({telemetry},set()),
 'posthog-host-only.ts':(set(),{telemetry}),
 'xampp-current.js':({server},set()),
}
for name,(required,forbidden) in checks.items():
    got=files[name]
    assert required<=got,(name,'missing',required-got)
    assert not forbidden&got,(name,'unexpected',forbidden&got)
print(f'{len(checks)} positive and near-miss cases passed')
