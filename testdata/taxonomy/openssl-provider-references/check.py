#!/usr/bin/env python3
"""Check reference placement and retained ancestor selection without loading code."""
import re
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
PROVIDER = 'micro-behaviors/crypto/provider::'
CONTEXT = 'micro-behaviors/crypto/library/implementation::crypto-library-context'
NETWORK = 'micro-behaviors/dylib/library/family::network-lib-marker'
CASES = [
    ('libcrypto', 'library_name = "libcrypto.so"\n',
     {PROVIDER + 'libcrypto-ref', CONTEXT, NETWORK},
     {PROVIDER + 'openssl-evp-pkey-api-reference'}),
    ('evp-pkey', 'api_name = "EVP_PKEY_new"\n',
     {PROVIDER + 'openssl-evp-pkey-api-reference', CONTEXT},
     {PROVIDER + 'libcrypto-ref', NETWORK}),
    ('near-miss', 'library_name = "libcurl.so"\n',
     {NETWORK},
     {PROVIDER + 'libcrypto-ref', PROVIDER + 'openssl-evp-pkey-api-reference', CONTEXT}),
]
with tempfile.TemporaryDirectory() as temporary:
    for name, source, expected, excluded in CASES:
        path = Path(temporary) / (name + '.dll')
        base = ROOT / 'testdata/benign/dotnet-default-manifest.dll'
        path.write_bytes(base.read_bytes() + b'\0' + source.encode() + b'\0')
        requested = sorted(expected | excluded)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             'test-rules', str(path), '--rules', ','.join(requested)],
            check=True, capture_output=True, text=True)
        # Transparent any-groups can be filtered from ordinary reports while
        # remaining eligible for directory selectors. Trace their evaluation.
        matched = set(re.findall(r'^MATCHED (\S+)', result.stdout, re.MULTILINE))
        not_matched = set(re.findall(r'^NOT MATCHED (\S+)', result.stdout, re.MULTILINE))
        assert expected <= matched, (name, expected - matched, result.stdout)
        assert excluded <= not_matched, (name, excluded - not_matched, result.stdout)
        print(name + ': passed')
