#!/usr/bin/env python3
"""Reject retired non-process taxonomy branches and their live references."""
import argparse
import re
from pathlib import Path

RETIRED = {
    'micro-behaviors/os/env/enumeration':
        'Use environment enumeration.',
    'micro-behaviors/os/env/dump':
        'Use environment enumeration or the supported collection objective.',
    'micro-behaviors/os/env/modify':
        'Use environment writes.',
    'micro-behaviors/os/env/check':
        'Use environment tests.',
    'micro-behaviors/os/env/gate':
        'Use environment tests or supported conditional behavior.',
    'micro-behaviors/os/env/user-paths':
        'Use environment paths or the observed path subject.',
    'micro-behaviors/os/service/driver':
        'Use kernel driver operations.',
    'micro-behaviors/dylib/library':
        'Use the library identity, capability, or observed symbol.',
    'micro-behaviors/ui/framework':
        'Use the framework identity or supported UI capability.',
    'objectives/collection/email-harvest':
        'Use email collection.',
    'objectives/credential-access/windows-registry':
        'Use registry credential access.',
    'objectives/lateral-movement/social-engineering/spam':
        'Use spam impact.',
    'objectives/lateral-movement/delivery':
        'Use the remote operation or supported objective.',
    'objectives/exfiltration/stealer/network-config':
        'Use system-information network theft.',
    'objectives/exfiltration/stealer/process-list':
        'Use system-information process theft.',
    'objectives/exfiltration/stealer/surveillance':
        'Classify by the stolen item or supported observation.',
    'objectives/exfiltration/stealer/phish':
        'Classify by the stolen item or acquisition behavior.',
    'objectives/supply-chain/install-hook':
        'Classify by supported execution or other objective.',
    'objectives/supply-chain/recon-exfil':
        'Classify discovery or export by supported result.',
    'objectives/supply-chain/credential-theft':
        'Classify credential acquisition or export by source.',
    'objectives/supply-chain/metadata-anomaly':
        'Classify package metadata, destructive behavior, or masquerade.',
    'objectives/anti-static/obfuscation/binary-metrics':
        'Use binary measurements or supported concealment.',
    'objectives/anti-static/obfuscation/code-metrics':
        'Use code measurements or supported concealment.',
    'objectives/anti-static/obfuscation/tools':
        'Use known tools or supported concealment.',
    'objectives/anti-static/obfuscation/multi-layer':
        'Use named concealment or representation observations.',
    'metadata/file/string':
        'Classify each string by its observed subject.',
    'metadata/file/literal':
        'Classify each literal by its type or observed subject.',
    'metadata/file/function':
        'Use function naming, declaration, population, or binary anatomy.',
    'metadata/file/arithmetic':
        'Use arithmetic operations or measured syntax properties.',
    'metadata/hardening/missing':
        'Use the mitigation subject or verified linking facts.',
    'metadata/binary/installer':
        'Use installer identity or the supported binary property.',
    'metadata/binary/framework':
        'Use framework identity or the supported capability.',
    'metadata/binary/vendor':
        'Use vendor observations or verified signatures.',
    'metadata/binary/signing':
        'Use signing or verified signature subjects.',
    'metadata/binary/license':
        'Use license observations by subject.',
    'metadata/binary/toolchain':
        'Use known toolchain or compiler observations.',
    'objectives/credential-access/theft/authentication':
        'Classify authentication evidence by credential source, acquisition, or supporting observation.',
    'metadata/file/encoded':
        'Use file encoding observations.',
    'metadata/lang/encoded':
        'Use language encoding observations.',
    'micro-behaviors/data/db/sql':
        'Classify database operations or SQL syntax by their subject.',
    'objectives/exfiltration/serialization':
        'Use credential export or data serialization by supported behavior.',
    'micro-behaviors/os/network':
        'Classify network operations under network or communications.',
    'micro-behaviors/communications/ipc/irc':
        'Classify IRC operations under communications/irc.',
    'micro-behaviors/crypto/library':
        'Classify by crypto operation, primitive, provider, or observed name.',
    'micro-behaviors/crypto/native':
        'Use crypto provider or the supported operation.',
    'micro-behaviors/crypto/asymmetric/key':
        'Use crypto key operations or representation.',
    'micro-behaviors/crypto/asymmetric/ecdh':
        'Use crypto key exchange.',
    'micro-behaviors/data/source':
        'Classify source syntax, control flow, or metaprogramming by subject.',
    'micro-behaviors/data/encoded':
        'Use encoding observations or decoding operations.',
    'micro-behaviors/fs/shell-ops':
        'Use the supported file operation, UI, or shell namespace.',
    'micro-behaviors/fs/traversal':
        'Use directory traversal or the evidenced filesystem operation.',
    'micro-behaviors/fs/directory/mkdir':
        'Use directory creation.',
    'micro-behaviors/mem/decompress':
        'Use data decompression by algorithm.',
    'micro-behaviors/process/threading':
        'Use thread, synchronization, work, or IPC operations.',
    'micro-behaviors/process/fork':
        'Use process creation by fork.',
    'micro-behaviors/process/user':
        'Use process identity or user administration.',
    'micro-behaviors/process/interpreter/reflection':
        'Use metaprogramming reflection.',
    'micro-behaviors/process/script':
        'Use the observed interpreter or execution mechanism.',
    'micro-behaviors/os/registry/manipulate':
        'Classify registry operations or their supported objective.',
    'objectives/command-and-control/dropper':
        'Classify payload execution, staging, or communication by outcome.',
    'objectives/exfiltration/sensitive-data':
        'Classify collection, credential acquisition, or export by evidence.',
    'metadata/lang/source/literal/value':
        'Classify literals by type, subject, or known identity.',
    'metadata/file/data-blob':
        'Classify the observed binary or text property.',
    'metadata/file/policy':
        'Classify policy evidence by subject.',
    'metadata/package/tooling':
        'Classify build, package, or known-tool evidence.',
    'well-known/malware/supply-chain':
        'Classify known malware by its defining role.',
}
REFERENCE = re.compile(r"^\s*(?:-\s*)?id:\s*['\"]?([^\s'\"#]+)")


def violations(root):
    for retired, guidance in RETIRED.items():
        branch = root / retired
        if branch.is_dir() and any(p.is_file() and p.suffix in ('.yaml', '.yml') for p in branch.rglob('*')):
            yield f'{retired}: retired taxonomy branch; {guidance}'
    for tier in ('metadata', 'micro-behaviors', 'objectives', 'well-known'):
        base = root / tier
        if not base.is_dir():
            continue
        for path in base.rglob('*'):
            if not path.is_file() or path.suffix not in ('.yaml', '.yml'):
                continue
            for number, line in enumerate(path.read_text().splitlines(), 1):
                match = REFERENCE.match(line)
                if not match:
                    continue
                reference = match.group(1).split('::', 1)[0].rstrip('/')
                for retired in RETIRED:
                    if reference == retired or reference.startswith(retired + '/'):
                        yield f'{path.relative_to(root)}:{number}: retired taxonomy reference {match.group(1)}'
                        break


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--traits-dir', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    errors = list(violations(args.traits_dir))
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    count = len(RETIRED)
    branch = 'branch' if count == 1 else 'branches'
    print(f'Legacy taxonomy: {count} retired {branch} and live references absent.')


if __name__ == '__main__':
    main()
