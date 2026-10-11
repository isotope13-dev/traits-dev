"""Regenerate inert archive controls; never execute the package."""
import gzip
import io
import json
from pathlib import Path
import re
import tarfile

ROOT = Path(__file__).resolve().parents[2]
with tarfile.open(ROOT / "testdata/hostile/api-anthropic-0.1.1.tgz") as archive:
    original = {
        item.name: archive.extractfile(item).read().decode()
        for item in archive.getmembers() if item.isfile()
    }


def write(destination, members):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        for name, source in sorted(members.items()):
            content = source.encode()
            entry = tarfile.TarInfo(name)
            entry.size, entry.mode, entry.mtime = len(content), 0o644, 0
            archive.addfile(entry, io.BytesIO(content))
    (ROOT / destination).write_bytes(gzip.compress(buffer.getvalue(), mtime=0))


def replace_once(source, before, after):
    assert source.count(before) == 1, before
    return source.replace(before, after)


configuration = "package/dist/configure.js"
key_declaration = '    const key = typeof env.ANTHROPIC_API_KEY === "string" ? env.ANTHROPIC_API_KEY : "";'
guarded = dict(original)
guarded[configuration] = replace_once(guarded[configuration], key_declaration,
    '    if (env.ANTHROPIC_BASE_URL !== GATEWAY_URL)\n'
    '        return { baseUrlConfigured: false, keyValid: null };\n' + key_declaration)
write("testdata/benign/ai-gateway-origin-guard.tgz", guarded)

explicit = dict(original)
explicit[configuration] = replace_once(explicit[configuration], key_declaration,
    '    const key = "EXPLICIT_TEST_GATEWAY_KEY";')
write("testdata/benign/ai-gateway-explicit-probe-key.tgz", explicit)

local = dict(original)
local["package/dist/sugarball.js"] = replace_once(local["package/dist/sugarball.js"],
    'res = await fetch(`${GATEWAY_URL}/v1/models`, {\n'
    '            method: "GET",\n'
    '            headers: { "x-api-key": key, "anthropic-version": "2023-06-01" },\n'
    '        });',
    'res = { status: key ? 200 : 401, json: async () => ({ data: [] }) };')
write("testdata/benign/ai-gateway-local-key-probe.tgz", local)

no_rewrite = dict(original)
for assignment in [
    '    env.ANTHROPIC_BASE_URL = GATEWAY_URL;\n',
    '    env.ANTHROPIC_API_KEY = trimmed;\n',
]:
    no_rewrite[configuration] = replace_once(no_rewrite[configuration], assignment, '')
write("testdata/hostile/ai-gateway-probe-without-rewrite.tgz", no_rewrite)

renamed = dict(original)
renames = {
    'validateKey': 'checkCredential', 'GATEWAY_URL': 'API_ORIGIN',
    'key': 'credential', 'keyValid': 'accepted', 'v': 'answer',
    'baseUrlConfigured': 'originMatches',
}
for name, source in list(renamed.items()):
    if name.endswith('.js'):
        source = re.sub(r'(?<![-\w])(' + '|'.join(renames) + r')(?![-\w])',
                        lambda match: renames[match.group()], source)
        source = source.replace('https://api-anthropic.help', 'https://anthropic-relay.example')
    renamed[name] = source
manifest = json.loads(renamed['package/package.json'])
manifest['name'] = 'gateway-health-helper'
manifest['bin'] = {'gateway-health-helper': 'dist/cli.js'}
renamed['package/package.json'] = json.dumps(manifest)
write("testdata/hostile/ai-gateway-renamed-probe.tgz", renamed)
