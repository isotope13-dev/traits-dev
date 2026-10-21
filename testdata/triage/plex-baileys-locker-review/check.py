"""Static regression controls; generated PE files have no managed entry.

Run: python3 check.py <scratch-directory> [sample-directory]
No PE or JavaScript is executed. Real specimens stay outside the repository.
"""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'fixture', ROOT / 'testdata/managed-records-review/verify.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
MICRO = 'micro-behaviors/'
PAIR = MICRO + 'communications/messaging/channel::'
OLD_PAIR = 'objectives/credential-access/messaging/whatsapp::'
FAMILY = 'well-known/malware/ransomware/hiddentears::'
EXTORT = 'objectives/impact/ransom/extortion::labeled-static-key-ransom-encryptor'
ASSOC = MICRO + 'os/registry/association::managed-file-handler-registration-references'
HIJACK = 'objectives/persistence/system/registry/surface::managed-keylogger-file-association-selfpath-references'
POLICY = MICRO + 'os/registry/keys/policy::'
ANTIAV = 'objectives/evasion/anti-av/registry::'


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    cases = []

    def case(name, data, yes, no=()):
        path = out / name
        path.write_bytes(data.encode() if isinstance(data, str) else data)
        cases.append((path, dict(yes), set(no)))

    labels = ['HiddenTearsKey123', 'HiddenTearsMutex']
    crypto = ['CreateEncryptor', 'CryptoStream']
    ransom = ['Your files have been encrypted']
    old_family = FAMILY + 'hiddentears-key123-template-ransomware'
    case('labeled-ransom.exe', fixture.build_pe(labels + crypto + ransom),
         {EXTORT: 5}, [old_family, FAMILY + 'hiddentears-template-ransomware'])
    case('labels-only.exe', fixture.build_pe(labels), {}, [EXTORT, old_family])
    case('crypto-without-ransom.exe', fixture.build_pe(labels + crypto), {}, [EXTORT])
    case('original-family.exe', fixture.build_pe(crypto +
         ['hidden_tear', 'Files have been encrypted with hidden tear']),
         {FAMILY + 'hiddentears-template-ransomware': 5}, [EXTORT])

    setters = ['ClassesRoot', 'RegistryKey', 'CreateSubKey', 'SetValue',
               'ExampleClass\\shell\\open\\command', 'get_ExecutablePath']
    case('document-handler.exe', fixture.build_pe(setters), {ASSOC: 3}, [HIJACK])
    case('keylogger-handler.exe', fixture.build_pe(setters + fixture.KEYLOG_MARKERS),
         {ASSOC: 3, HIJACK: 5})
    case('keylogger-without-hive.exe', fixture.build_pe(
         [x for x in setters if x != 'ClassesRoot'] + fixture.KEYLOG_MARKERS),
         {}, [ASSOC, HIJACK])
    case('keylogger-without-setter.exe', fixture.build_pe(
         [x for x in setters if x != 'SetValue'] + fixture.KEYLOG_MARKERS),
         {}, [ASSOC, HIJACK])
    case('handler-without-selfpath.exe', fixture.build_pe(
         [x for x in setters if x != 'get_ExecutablePath'] + fixture.KEYLOG_MARKERS),
         {ASSOC: 3}, [HIJACK])

    policy = 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender'
    realtime = 'HKLM:\\SOFTWARE\\Microsoft\\Windows Defender\\Real-Time Protection'
    case('policy-reference.ps1', "$path = '" + policy + "'", {POLICY + 'defender-policy-registry-key-reference': 3},
         [ANTIAV + 'defender-antispyware-registry-tampering'])
    case('policy-disable.ps1', "Set-ItemProperty -Path '" + policy +
         "' -Name DisableAntiSpyware -Value 1", {ANTIAV + 'defender-antispyware-registry-tampering': 5})
    case('realtime-disable.ps1', "Set-ItemProperty -Path '" + realtime +
         "' -Name DisableRealTimeProtection -Value 1", {ANTIAV + 'defender-realtime-registry-tampering': 5})

    direct = 'fixed-whatsapp-pairing-code-in-socket-client'
    archive = 'archive-embedded-pairing-code-socket-default'
    js = "const pairingCode = 'ABCD1234'; sendNode({tag:'link_code_companion_reg'});"
    case('fixed-pairing.js', js, {PAIR + direct: 3}, [OLD_PAIR + direct])
    case('caller-pairing.js', js.replace("'ABCD1234'", 'callerCode'), {},
         [PAIR + direct, OLD_PAIR + direct])
    path = out / 'fixed-pairing-config.tgz'
    with tarfile.open(path, 'w:gz') as tar:
        for name, data in [('package/package.json', '{"name":"pairing-control","version":"1.0.0","type":"module"}'),
                           ('package/lib/config.js', "export const customConfig = {pairingCode:'ABCD1234'};"),
                           ('package/lib/wrapper.js', 'sock.requestPairingCode = (phone, custom) => original(phone, custom ?? customConfig.pairingCode);'),
                           ('package/lib/socket.js', "sendNode({tag:'link_code_companion_reg'});")]:
            blob = data.encode()
            member = tarfile.TarInfo(name)
            member.size = len(blob)
            tar.addfile(member, io.BytesIO(blob))
    cases.append((path, {PAIR + archive: 3}, {OLD_PAIR + archive}))

    if len(sys.argv) > 2:
        samples = Path(sys.argv[2])
        cases.append((samples / '1ae6898b491a/romagnagazzette.com_chrome.exe',
                      {EXTORT: 5, HIJACK: 5, ASSOC: 3}, {old_family}))
        cases.append((samples / 'fbe6ab60c54a/@randev404-baileys-1.0.1.tgz',
                      {PAIR + archive: 3,
                       'objectives/impact/ui/manipulation/social::archive-sidecar-session-open-newsletter-follow': 5,
                       'objectives/supply-chain/trojanized/library/fork-branding::whatsapp-library-fork-sidecar-session-open-newsletter-follow': 5},
                      {OLD_PAIR + archive}))
    real_other = out.parent / 'randev100.tgz'
    if real_other.exists():
        cases.append((real_other, {PAIR + archive: 3,
                      'objectives/impact/ui/manipulation/social::archive-sidecar-session-open-newsletter-follow': 5},
                      {OLD_PAIR + archive}))

    result = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--json',
                             *(str(p) for p, _, _ in cases)],
                            capture_output=True, text=True, check=True)
    (out / 'scan.jsonl').write_text(result.stdout)
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    observed = {f['path']: {t['id']: t['crit'] for t in f.get('traits', [])}
                for report in reports for f in report['files']}
    assertions = 0
    for path, yes, no in cases:
        actual = observed[str(path)]
        for id, severity in yes.items():
            assert actual.get(id) == severity, (path.name, id, severity, actual.get(id))
        assert not no.intersection(actual), (path.name, sorted(no.intersection(actual)))
        assertions += len(yes) + len(no)
    print(f'{len(cases)} cases, {assertions} trait assertions passed')


if __name__ == '__main__':
    main()
