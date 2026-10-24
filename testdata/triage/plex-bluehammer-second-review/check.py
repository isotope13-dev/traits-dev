#!/usr/bin/env python3
"""Static regression checks; generated programs and request payloads are never run."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        yield value
        text = text[end:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='acquit-controls-') as directory:
        out = Path(directory)
        for name, source in json.loads((HERE / 'controls.json').read_text()).items():
            (out / name).write_text(source)
        for stem in ('h264-exact', 'h264-accessor', 'h264-nearmiss'):
            subprocess.run(['cc', str(out / (stem + '.c')), '-o',
                            str(out / (stem + '.bin'))], check=True)
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT),
                                 '--format=json'] + [str(p) for p in sorted(out.iterdir())],
                                capture_output=True, text=True, check=True)
        files = {Path(f['path']).name: {t['id']: t['crit'] for t in f.get('traits', [])}
                 for report in documents(result.stdout) for f in report['files']}
        assert len(files) == 21, len(files)
        ssrf = 'objectives/execution/exploit/access-control::plex-timeline-loopback-agent-ssrf'
        leak = 'objectives/exfiltration/stealer/token::plex-agent-loopback-prefix-token-leak'
        write = 'objectives/execution/exploit/code-injection::plex-transcoder-codec-library-write'
        h264 = 'micro-behaviors/communications/http/query::plex-transcoder-h264-options'
        header = 'micro-behaviors/communications/http/auth::plex-token-header-line'
        get = 'micro-behaviors/communications/http/get::get'
        key = 'micro-behaviors/os/registry/open::offreg-open-key-call'
        catalog = 'micro-behaviors/communications/http/query::vite-fs-bypass-query-catalog'
        click = 'micro-behaviors/communications/http/query::affiliate-click-account-url'
        assert all(files['plex-sender.ps1'][i] == 5 for i in (ssrf, leak, write))
        assert leak not in files['plex-loopback-only.ps1']
        assert files['plex-loopback-only.ps1'][ssrf] == 5
        assert write not in files['plex-video-output.ps1']
        assert h264 in files['plex-video-output.ps1']
        for name in ('plex-status.rb', 'plex-normal-subscribe.http', 'get-only.http',
                     'get-nearmiss.txt', 'offreg-declaration.rs', 'offreg-call.rs',
                     'click-url.html', 'click-nearmiss.html', 'vite-nearmiss.py'):
            assert not any(c >= 4 for c in files[name].values()), name
        assert {get, header} <= files['plex-normal-subscribe.http'].keys()
        assert get in files['get-only.http']
        assert get not in files['get-nearmiss.txt'] and header not in files['get-nearmiss.txt']
        assert key in files['offreg-call.rs'] and key not in files['offreg-declaration.rs']
        assert catalog in files['vite-catalog.py'] and catalog not in files['vite-nearmiss.py']
        assert files['vite-secret-scanner.py'][
            'objectives/credential-access/files/secret-sweep::vite-fs-secret-wordlist-scanner'] == 5
        assert click in files['click-url.html'] and click not in files['click-nearmiss.html']
        assert h264 in files['h264-exact.c']
        for name in ('h264-exact.bin', 'h264-accessor.bin'):
            assert h264 + '-binary' in files[name], name
        assert h264 + '-binary' not in files['h264-nearmiss.bin']
        print(json.dumps({'controls_passed': len(files)}, indent=2))


if __name__ == '__main__':
    main()
