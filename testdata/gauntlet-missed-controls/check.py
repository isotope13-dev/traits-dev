"""Check configuration capabilities without inferring secret theft."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='/home/t/.local/bin/cleave')
parser.add_argument('--case', action='append', help='Run only named cases (repeatable)')
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
repo = fixtures.parent.parent
cookie = 'micro-behaviors/communications/http/cookies::'
walk = 'micro-behaviors/fs/directory/traverse::python-dotenv-walk-load-context'
xor = 'micro-behaviors/data/decode/xor::aliased-charcode-xor-rebuild'
frame = 'micro-behaviors/communications/http/client/resource::one-pixel-external-frame'
dispatch = 'objectives/anti-static/obfuscation/string/reconstruct::wsh-aliased-xor-computed-dispatch'
markup = 'micro-behaviors/ui/window/insert-html::'
rathole = 'well-known/dual-use/tunnel/rathole::rathole-namespace'
metadata = 'metadata/package/documentation/claims::'
indexed = 'objectives/anti-static/obfuscation/string/reconstruct::'
cases = {
    'configured-cookie.py': {walk, cookie + 'python-dotenv-cookie-get-context'},
    'configured-request.py': set(),
    'local-dotenv.py': {walk},
    'alias-xor.js': {xor},
    'alias-xor-block.js': {xor},
    'different-alias.js': set(),
    'tracking-frame.html': {frame},
    'visible-frame.html': set(),
    'shortcut-editor.js': {'micro-behaviors/ui/window/insert-html::shortcut-storage-and-link-markup'},
    'wsh-xor-dispatch.js': {xor, dispatch},
    'remote-links.js': {markup + n for n in ('json-response-and-link-body-markup',
                        'json-response-and-paragraph-markup', 'json-response-and-link-insertion',
                        'json-response-and-anchor-target-markup')},
    'text-links.js': set(),
    'PKG-INFO': {metadata + 'pypi-metadata-npm-import-syntax', metadata + 'pypi-metadata-formatcolor-utility-claim'},
    'ordinary/PKG-INFO': set(),
    'setup.py': set(),
    'rathole.elf': {rathole},
    'other-tunnel.elf': set(),
    'indexed-analytics.rs': {indexed + 'rust-charset-index-string-rebuild',
                             indexed + 'indexed-string-network-analytics'},
    'ordinary-build.rs': set(),
    'packed_module-1.0.0-py3-none-any.whl': set(),
    'worker-reversed.js': {indexed + 'worker-reversed-script-reference'},
    'worker-unrelated.js': set(),
    'command-form.pl': {'micro-behaviors/ui/controls/input::html-command-action-field'},
    'ordinary-form.pl': set(),
    'mirc-profile.ini': set(),
    'irc-settings.ini': {'micro-behaviors/communications/irc/configure::mirc-server-endpoint-declaration'},
    'irc-labels.ini': set(),
    'mirc-paths.ini': {'micro-behaviors/fs/path/system::mirc-windows-system-directory-reference',
                       'micro-behaviors/fs/path/config/system::mirc-reg-file-reference'},
    'mirc-paths-nearmiss.ini': set(),
    'cgi-interface.so': {'objectives/command-and-control/backdoor/webshell/request/command::preload-cgi-command-shell-interface'},
    'cgi-no-command.so': set(),
    'cgi-no-preload.so': set(),
    'bnc-flood-bot-variables.txt': {
        'micro-behaviors/data/config/schema::mirc-numbered-variable-assign',
        'micro-behaviors/fs/path/config/system::mirc-reg-file-reference',
        *('objectives/command-and-control/channel/irc/bot::' + suffix for suffix in
          ('mirc-flood-server-var', 'mirc-flood-port-var', 'mirc-flood-channel-var',
           'mirc-proxy-download-var', 'mirc-scan-range-var')),
    },
}
env = dict(os.environ, CLEAVE_NO_UPDATE_CHECK='1', XDG_CACHE_HOME='/tmp/gauntlet-cache', RAYON_NUM_THREADS='2')
if args.case:
    unknown = set(args.case) - cases.keys()
    if unknown:
        parser.error('Unknown cases: ' + ', '.join(sorted(unknown)))
    cases = {name: required for name, required in cases.items() if name in args.case}
with tempfile.TemporaryDirectory(prefix='gauntlet-controls-') as tmp:
    for name, required in cases.items():
        target = Path(tmp) / name
        target.parent.mkdir(exist_ok=True)
        if name.startswith('cgi-') and name.endswith('.so'):
            parameter = 'mode=' if name == 'cgi-no-command.so' else 'cmd='
            preload = 'OTHER_ENV' if name == 'cgi-no-preload.so' else 'LD_PRELOAD'
            # Harmless data/API-reference controls: compile but never load them.
            # There is no request-to-shell flow. The composite must remain
            # suspicious, not hostile, even when every observation is present.
            source = ('#include <stdlib.h>\n'
                      'const char query[] = "QUERY_STRING=";\n'
                      'const char parameter[] = "' + parameter + '";\n'
                      'const char preload[] = "' + preload + '";\n'
                      'int (*shell_api)(const char *) = system;\n'
                      'int (*env_api)(const char *) = unsetenv;\n')
            subprocess.run(['cc', '-shared', '-fPIC', '-x', 'c', '-o', str(target), '-'],
                           input=source, text=True, capture_output=True, check=True)
        elif name in ('rathole.elf', 'other-tunnel.elf'):
            marker = 'rathole::client' if name == 'rathole.elf' else 'other_tunnel::client'
            # Compile a harmless native control without executing it. Native
            # platform filtering must be tested on a native image, not JS.
            source = 'const char identity[] = "' + marker + '"; const char padding[101000] = {1}; int main(void) { return identity[0] + padding[0]; }'
            subprocess.run(['cc', '-x', 'c', '-o', str(target), '-'], input=source,
                           text=True, capture_output=True, check=True)
        elif name == 'packed_module-1.0.0-py3-none-any.whl':
            with zipfile.ZipFile(target, 'w') as archive:
                archive.writestr('packed_module/__init__.py', (fixtures / 'packed-module.py').read_text())
                archive.writestr('packed_module-1.0.0.dist-info/WHEEL', 'Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
                archive.writestr('packed_module-1.0.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: packed-module\nVersion: 1.0.0\n')
        else:
            source = {'PKG-INFO': fixtures / 'example.PKG-INFO',
                      'ordinary/PKG-INFO': fixtures / 'ordinary.PKG-INFO',
                      'setup.py': fixtures / 'hex-setup.py',
                      'indexed-analytics.rs': repo / 'testdata/cargo-build-analytics-exfil/evil-build.rs',
                      'ordinary-build.rs': repo / 'testdata/cargo-build-analytics-exfil/benign-build.rs'}.get(name, fixtures / name)
            if name == 'bnc-flood-bot-variables.txt':
                source = repo / 'testdata/purgatory/mirc-saved-variables' / name
            shutil.copyfile(source, target)
        run = subprocess.run([args.cleave, '--no-update-check', '--traits-dir', str(repo),
                              '--format', 'json', 'analyze', str(target)],
                             env=env, check=True, capture_output=True, text=True, timeout=90)
        report = json.loads(run.stdout)
        traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
        assert required <= traits.keys(), (name, required - traits.keys())
        alerts = [t['id'] for t in traits.values() if t.get('crit', 0) >= 4]
        expected_alerts = {dispatch} if name == 'wsh-xor-dispatch.js' else set()
        if name == 'indexed-analytics.rs':
            expected_alerts = {indexed + 'rust-charset-index-string-rebuild', indexed + 'indexed-string-network-analytics'}
        if name == 'worker-reversed.js':
            expected_alerts = {indexed + 'worker-reversed-script-reference'}
        if name == 'mirc-profile.ini':
            expected_alerts = {'objectives/evasion/masquerade/extension-mismatch::mirc-dll-suffixed-script-config'}
        if name == 'cgi-interface.so':
            expected_alerts = required
        if name == 'packed_module-1.0.0-py3-none-any.whl':
            assert alerts, 'Packed Python must remain visible for review'
            assert not any(t.get('crit') == 5 for t in traits.values()), (name, alerts)
        else:
            assert set(alerts) == expected_alerts, (name, alerts)
        if name != 'configured-cookie.py':
            assert cookie + 'python-dotenv-cookie-get-context' not in traits, name
        if name == 'different-alias.js':
            assert xor not in traits, name
        if name == 'visible-frame.html':
            assert frame not in traits, name
        if name == 'other-tunnel.elf':
            assert rathole not in traits, name
        if name == 'text-links.js':
            assert markup + 'json-response-and-paragraph-markup' not in traits, name
        if name == 'worker-unrelated.js':
            assert indexed + 'worker-reversed-script-reference' not in traits, name
        if name == 'ordinary-form.pl':
            assert 'micro-behaviors/ui/controls/input::html-command-action-field' not in traits, name
        if name == 'irc-labels.ini':
            assert 'micro-behaviors/communications/irc/configure::mirc-server-endpoint-declaration' not in traits, name
        if name == 'mirc-paths-nearmiss.ini':
            assert 'micro-behaviors/fs/path/system::mirc-windows-system-directory-reference' not in traits, name
            assert 'micro-behaviors/fs/path/config/system::mirc-reg-file-reference' not in traits, name
        if name == 'ordinary/PKG-INFO':
            assert metadata + 'pypi-metadata-formatcolor-utility-claim' not in traits, name
        print(f'PASS {name}: expected capabilities and criticality', flush=True)
