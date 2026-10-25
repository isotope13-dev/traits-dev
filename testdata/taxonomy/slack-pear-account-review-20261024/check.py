"""Static regression scans only; never run source fixtures or package hooks."""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SELF = 'objectives/evasion/self-delete/scripts::go-tasking-loop-self-delete'
ARGV = 'micro-behaviors/fs/delete/file/self::go-remove-argv-zero'
SLACK = 'objectives/command-and-control/backdoor/control/slack::go-slack-polled-chunked-tasking'
CHANNEL = 'objectives/command-and-control/backdoor/implant::go-slack-encrypted-command-channel'
ENV = 'objectives/exfiltration/stealer/env::javascript-env-credential-oob-http-exfil'
PATCH = 'objectives/supply-chain/trojanized/library/runtime-patch::node-modules-credential-exfil-source-injection'
CONTEXT = 'micro-behaviors/os/package-manager/hook-install::npm-postinstall-oob-https-context'
PEAR = 'objectives/execution/exploit/include-gadget::python-pear-request-command-injection'
ENCODE = 'micro-behaviors/data/encode/url::percent-sign-reescape'


def unpack(text):
    decoder = json.JSONDecoder()
    while text.strip():
        obj, used = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[used:]
        yield from obj['files']


def main():
    # Keep fixture basenames, but avoid testdata-based exemptions on copies.
    with tempfile.TemporaryDirectory(prefix='registry-second-', dir=sys.argv[1]) as temp:
        dest = Path(temp)
        for name in ['rat.go', 'pear.py', 'audit.tgz']:
            (dest / name).write_bytes((HERE / name).read_bytes())
        rat = (HERE / 'rat.go').read_text()
        (dest / 'decode-percent.py').write_text("text.replace('%25', '%')\n")
        (dest / 'unrelated-percent.py').write_text("text.replace('%', 'percent'); other.replace('x', '%25')\n")
        (dest / 'argv-one.go').write_text(rat.replace('os.Remove(os.Args[0])', 'os.Remove(os.Args[1])'))
        (dest / 'no-agent.go').write_text('''package main
import "os"
func main() { os.Remove(os.Args[0]) }
''')
        (dest / 'encrypted-slack-backup.go').write_text('''package main
import ("crypto/aes"; "crypto/cipher"; "os/exec")
const base = "https://slack.com/api/"
const history = "conversations.history"
const auth = "auth.test"
type packet struct { T string `json:"t"`; ID string `json:"id"`; D string `json:"d"` }
func main() {
 block, _ := aes.NewCipher(make([]byte, 32))
 aead, _ := cipher.NewGCM(block)
 _, _ = aead.Open(nil, make([]byte, 12), nil, nil)
 exec.Command("git", "status").Start()
}
''')
        with tarfile.open(dest / 'webhook-smoke.tgz', 'w:gz') as archive:
            members = {
                'package/package.json': json.dumps({'name': 'webhook-smoke', 'version': '1.0.0', 'scripts': {'postinstall': 'node index.js'}}),
                'package/index.js': "const https = require('https'); const req = https.request('https://webhook.site/11111111-1111-4111-8111-111111111111', {method:'POST'}); req.write(JSON.stringify({event:'smoke-test'})); req.end();",
            }
            for name, content in members.items():
                data = content.encode()
                info = tarfile.TarInfo(name)
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', str(dest)], capture_output=True, text=True, check=True)
        files = {Path(f['path']).name: f for f in unpack(result.stdout)}
        checks = 0
        def expect(name, present=(), absent=()):
            nonlocal checks
            traits = {t['id']: t for t in files[name].get('traits', [])}
            for id in present:
                assert id in traits, (name, 'missing', id)
                checks += 1
            for id in absent:
                assert id not in traits, (name, 'unexpected', id)
                checks += 1
            return traits
        expect('rat.go', [ARGV, SELF, SLACK, CHANNEL])
        expect('argv-one.go', [SLACK, CHANNEL], [ARGV, SELF])
        expect('no-agent.go', [ARGV], [SELF, SLACK, CHANNEL])
        expect('encrypted-slack-backup.go', absent=[SELF, SLACK, CHANNEL])
        expect('pear.py', [PEAR, ENCODE])
        expect('decode-percent.py', absent=[ENCODE])
        expect('unrelated-percent.py', absent=[ENCODE])
        expect('audit.tgz', [ENV, PATCH, CONTEXT])
        smoke = expect('webhook-smoke.tgz', [CONTEXT], [ENV, PATCH])
        assert smoke[CONTEXT]['crit'] == 3
        checks += 1
        print(f'{checks} static regression assertions passed')


if __name__ == '__main__':
    main()
