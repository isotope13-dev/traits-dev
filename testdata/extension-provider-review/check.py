#!/usr/bin/env python3
"""Focused behavior controls, not reconstructed original extensions."""
import json
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRAND = 'objectives/evasion/masquerade/brand/product::amnezia-author-myxa-provider-substitution'
HEAD = 'micro-behaviors/communications/http/head::fetch-head-call'
FLOW = 'micro-behaviors/communications/proxy/config::proxy-config-consumes-resolver-result'
GATE = 'micro-behaviors/ui/controls/widget::premium-selection-modal-return'
COUNT = 'micro-behaviors/os/telemetry/activity::extension-tab-open-counter-write'
OLD_IDENTITY = 'objectives/supply-chain/impersonation/brand::amnezia-vpn-atlas-space-identity'
CLICK = 'micro-behaviors/ui/window/click::element-id-programmatic-click'
RELAY = 'micro-behaviors/communications/proxy/config::socks5-relay-lifecycle-control-actions'
cases = {}

with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
    temp = Path(temp)

    def source(name, content, required=(), forbidden=()):
        p = temp / name
        p.write_text(content)
        cases[name] = (p, set(required), set(forbidden))

    def bundle(name, author, label, proxy=True, manifest=None, commented=False):
        p = temp / name
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('manifest.json', json.dumps(manifest or {
                'manifest_version': 3, 'name': 'Independent relay', 'version': '2.0',
                'author': author, 'permissions': ['proxy'],
                'background': {'service_worker': 'renamed.js'},
            }, ensure_ascii=False))
            label = f'<span>{label}</span>'
            z.writestr('renamed.html', f'<!-- {label} -->' if commented else label)
            if proxy:
                # Existing out-of-batch control: ordinary user-activated proxy.
                z.writestr('renamed.js', (ROOT / 'testdata/benign/fake-vpn-relay-farm.js').read_text())
        return p

    for name, author, label, proxy, commented, hostile in [
        ('mixed-providers.zip', 'Амнезия Team', 'Myxa VPN', True, False, True),
        ('own-provider.zip', 'Myxa Team', 'Myxa VPN', True, False, False),
        ('same-provider.zip', 'Амнезия Team', 'Amnezia VPN', True, False, False),
        ('no-relay.zip', 'Амнезия Team', 'Myxa VPN', False, False, False),
        ('comment-label.zip', 'Амнезия Team', 'Myxa VPN', True, True, False),
    ]:
        p = bundle(name, author, label, proxy, commented=commented)
        cases[name] = (p, {BRAND} if hostile else set(), set() if hostile else {BRAND})

    p = bundle('retained-atlas-identity.zip', '', '', manifest={
        'manifest_version': 3, 'version': '1.0', 'name': 'Амнезия VPN',
        'short_name': 'Амнезия VPN', 'action': {'default_title': 'Амнезия VPN'},
        'author': 'Амнезия Team', 'homepage_url': 'https://atlasvpn.space/',
        'permissions': ['proxy'], 'background': {'service_worker': 'renamed.js'},
    })
    cases[p.name] = (p, {OLD_IDENTITY}, {BRAND})

    source('head.js', 'fetch(url, {method: "HEAD", redirect: "manual"});', [HEAD])
    source('head-comment.js', '// fetch(url, {method: "HEAD"});\nfetch(url);', forbidden=[HEAD])
    source('post.js', 'fetch(url, {method: "POST"}); const note="HEAD";', forbidden=[HEAD])
    source('resolver.js', 'async function connect(n){const ip=await resolveProxyHost(n);setProxyConfig(ip,n.port);}', [FLOW])
    source('unrelated-resolver.js', 'async function connect(n){const ip=await resolveProxyHost(n);setProxyConfig(n.host,n.port);}', forbidden=[FLOW])
    source('premium-gate.js', 'function pick(n){if(n.premium){showPremiumModal();render();return;}connect(n);}', [GATE])
    source('licensed-gate.js', 'function pick(n){if(n.premium&&!licensed){showPremiumModal();return;}connect(n);}', forbidden=[GATE])
    source('continuing-modal.js', 'function pick(n){if(n.premium){showPremiumModal();}connect(n);}', forbidden=[GATE])
    source('counter.js', 'chrome.storage.local.set({tabOpens: old+1});', [COUNT])
    source('counter-mention.js', '// chrome.storage.local.set({tabOpens: old+1});\nconst tabOpens=0;', forbidden=[COUNT])
    source('counter-read.js', 'chrome.storage.local.get("tabOpens",console.log);', forbidden=[COUNT])
    source('click.js', 'document.getElementById("ordinaryButton").click();', [CLICK])
    source('relay-actions.js', (ROOT / 'testdata/benign/fake-vpn-relay-farm.js').read_text() + '''
        chrome.runtime.onInstalled.addListener(()=>chrome.tabs.create({url:"https://example.org/"}));
        const actions=["RELAY_ENGAGE","RELAY_RELEASE","RELAY_POLL"];
    ''', [RELAY])

    proc = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json',
        *[str(p) for p, _, _ in cases.values()],
    ], check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    text = proc.stdout.lstrip()
    files = []
    while text:
        report, end = decoder.raw_decode(text)
        files.extend(report['files'])
        text = text[end:].lstrip()
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])} for f in files}
    for name, (_, required, forbidden) in cases.items():
        actual = found.get(name, set())
        assert required <= actual, (name, 'missing', required - actual)
        assert not forbidden & actual, (name, 'unexpected', forbidden & actual)
    print(f'{len(cases)} focused extension controls passed')
