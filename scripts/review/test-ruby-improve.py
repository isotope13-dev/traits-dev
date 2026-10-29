#!/usr/bin/env python3
"""Verify Ruby source/sink bindings without executing any sample code."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
WEB = 'objectives/command-and-control/backdoor/webshell/intercept/module::'
COOKIE = WEB + 'cookie-delivered-code-execution'
PRODUCTION = WEB + 'ruby-cookie-eval-with-production-check'
READ = 'micro-behaviors/fs/read/file/full::ruby-file-content-base64-value-flow'
PACKER = 'objectives/credential-access/credential-manager/secret-storage::ruby-encoded-credential-file-read'
INVENTORY = 'objectives/credential-access/files/secret-sweep::ruby-secret-file-hash-inventory'
RUNNER = 'micro-behaviors/process/create/subprocess::ruby-http-body-script-subprocess-flow'
TLS = 'objectives/command-and-control/dropper/delivery/fetch-exec::ruby-unverified-http-body-subprocess-exec'
CI_WRITE = 'micro-behaviors/os/env/cicd::ruby-github-env-preload-write'
CI_HOOK = 'objectives/supply-chain/trojanized/build-pipeline::ruby-credential-collector-ci-preload'


def objects(text):
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            return
        value, offset = decoder.raw_decode(text, offset)
        yield value


def main():
    cases = {}

    def add(name, source, required=(), forbidden=(), no_hostile=False):
        cases[name] = source, set(required), set(forbidden), no_hostile

    cookie = (ROOT / 'testdata/hostile/generated/ruby-improve/cookie-evaluator.rb').read_text()
    packer = (ROOT / 'testdata/hostile/generated/ruby-improve/credential-packer.rb').read_text()
    inventory = (ROOT / 'testdata/suspicious/generated/ruby-bad-review/recon-helper/sample.rb').read_text()
    runner = (ROOT / 'testdata/suspicious/generated/ruby-bad-review/unsafe-runner/sample.rb').read_text()
    ci = (ROOT / 'testdata/hostile/generated/ruby-bad-review/session-store/sample.rb').read_text()
    add('cookie.rb', cookie, [COOKIE, PRODUCTION])
    add('cookie-renamed.rb', re.sub(r'\bx\b', 'decoded_command', cookie), [COOKIE, PRODUCTION])
    direct = "def call(env)\n data = Base64.strict_decode64(env['HTTP_COOKIE'])\n eval(data)\nend\n"
    add('cookie-direct.rb', direct, [COOKIE])
    add('cookie-inline.rb', "def call(env)\n eval(Base64.decode64(env['HTTP_COOKIE']))\nend\n", [COOKIE])
    add('cookie-other-eval.rb', direct.replace('eval(data)', 'eval(template)'), forbidden=[COOKIE, PRODUCTION], no_hostile=True)
    add('cookie-display.rb', direct.replace('eval(data)', 'puts(data)'), forbidden=[COOKIE, PRODUCTION], no_hostile=True)
    add('cookie-other-header.rb', direct.replace('HTTP_COOKIE', 'HTTP_USER_AGENT'), forbidden=[COOKIE, PRODUCTION])
    add('quoted-cookie.rb', "puts <<'EXAMPLE'\n" + cookie + '\nEXAMPLE\n', forbidden=[COOKIE, PRODUCTION])
    add('comment-production.rb', '# Rails.env.production?\n' + direct, [COOKIE], [PRODUCTION])
    template = (ROOT / 'testdata/notable/controls/ruby-improve/production-template.rb').read_text()
    add('production-template.rb', template, forbidden=[COOKIE, PRODUCTION], no_hostile=True)
    add('packer.rb', packer, [READ, PACKER])
    add('packer-renamed.rb', re.sub(r'\bcontent\b', 'captured_bytes', re.sub(r'\bCREDENTIAL_FILES\b', 'TARGETS', packer)), [READ, PACKER])
    add('packer-different-read.rb', packer.replace('File.read(full_path)', "File.read('/tmp/public-data')"), forbidden=[PACKER])
    add('packer-different-encoding.rb', packer.replace('Base64.strict_encode64(content)', 'Base64.strict_encode64(status)'), forbidden=[READ, PACKER])
    add('ordinary-file-encoding.rb', "# .aws/credentials .ssh/id_rsa .netrc\ncontent = File.read('/tmp/public-data')\nencoded = Base64.strict_encode64(content)\n", [READ], [PACKER], True)
    add('inventory.rb', inventory, [INVENTORY], no_hostile=True)
    add('inventory-other-read.rb', inventory.replace('File.read(f)', "File.read('/tmp/public-data')"), forbidden=[INVENTORY], no_hostile=True)
    add('inventory-other-hash.rb', inventory.replace('Digest::SHA256.hexdigest(content)', 'Digest::SHA256.hexdigest(status)'), forbidden=[INVENTORY], no_hostile=True)
    add('runner.rb', runner, [RUNNER, TLS], no_hostile=True)
    add('runner-renamed.rb', re.sub(r'\bexecute_script\b', 'launch_text', re.sub(r'\bresp\b', 'reply', runner)), [RUNNER, TLS], no_hostile=True)
    add('runner-other-body.rb', runner.replace('execute_script(interpreter, resp.body)', 'execute_script(interpreter, trusted_script)'), forbidden=[RUNNER, TLS], no_hostile=True)
    add('runner-other-target.rb', runner.replace('execute_script(interpreter, resp.body)', 'display_script(interpreter, resp.body)'), forbidden=[RUNNER, TLS], no_hostile=True)
    add('runner-other-temp-path.rb', runner.replace('#{tf.path}', '#{other.path}'), forbidden=[RUNNER, TLS], no_hostile=True)
    add('runner-other-executed-command.rb', runner.replace("Open3.capture3({ 'PATH' => ENV['PATH'] }, cmd)", "Open3.capture3({ 'PATH' => ENV['PATH'] }, other_command)"), forbidden=[RUNNER, TLS], no_hostile=True)
    add('ci-preload.rb', ci, [CI_WRITE, CI_HOOK])
    add('ci-renamed.rb', re.sub(r'\bgenv\b', 'workflow_environment', ci), [CI_WRITE, CI_HOOK])
    add('ci-other-file.rb', ci.replace("File.open(genv, 'a')", "File.open(other, 'a')"), forbidden=[CI_WRITE, CI_HOOK])
    add('ci-overwrite.rb', ci.replace("File.open(genv, 'a')", "File.open(genv, 'w')"), forbidden=[CI_WRITE, CI_HOOK])
    add('ci-other-setting.rb', ci.replace('RUBYOPT=-r#{hook}', 'LOG_LEVEL=#{hook}'), forbidden=[CI_WRITE, CI_HOOK])
    add('ordinary-ci-preload.rb', "def configure\n path = ENV['GITHUB_ENV']\n File.open(path, 'a') { |output| output.puts \"RUBYOPT=-r#{profiler}\" }\nend\n", [CI_WRITE], [CI_HOOK], True)

    with tempfile.TemporaryDirectory(prefix='ruby-improve-') as temp:
        paths = []
        for name, (source, *_rest) in cases.items():
            path = Path(temp) / name
            path.write_text(source)
            paths.append(str(path))
        result = subprocess.run([os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave')),
                                 '--traits-dir', str(ROOT), '--format=json', *paths], capture_output=True, text=True, check=True)
        observed = {}
        for report in objects(result.stdout):
            for item in report['files']:
                observed.setdefault(Path(item['path']).name, []).extend(item.get('traits', []))
        failures = []
        for name, (_source, required, forbidden, no_hostile) in cases.items():
            traits = observed[name]
            ids = {t['id'] for t in traits}
            hostile = {t['id'] for t in traits if t['crit'] == 5}
            if required - ids or forbidden & ids or no_hostile and hostile:
                failures.append({'case': name, 'missing': sorted(required - ids),
                                 'unexpected': sorted(forbidden & ids), 'hostile': sorted(hostile) if no_hostile else []})
        assert not failures, json.dumps(failures, indent=2)
    print(f'Ruby improvement regressions passed: {len(cases)} cases')


if __name__ == '__main__':
    main()
