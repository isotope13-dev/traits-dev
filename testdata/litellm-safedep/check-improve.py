#!/usr/bin/env python3
"""Check incident-driven trait boundaries using inert, temporary source files.

Source snippets are inspected, never imported or executed. An optional sample
root adds the six verified payload files and the two safely decoded bodies.
"""
import argparse
import ast
import base64
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import tokenize
import zlib

ROOT = Path(__file__).resolve().parents[2]
BCRYPT = 'micro-behaviors/crypto/kdf/algorithm::bcrypt'
BCRYPT_REF = 'micro-behaviors/crypto/kdf/algorithm::bcrypt-password-reference'
BCRYPT_API = 'micro-behaviors/crypto/kdf/algorithm::python-bcrypt-password-api'
AES = 'micro-behaviors/crypto/symmetric/aes/mode::python-aes-cbc-cipher'
ENV = 'micro-behaviors/os/env/secret-name::python-environ-credential-selection'
SSH = 'micro-behaviors/communications/http/request/credentials::python-ssh-listing-upload-context'
HOST = 'micro-behaviors/communications/http/telemetry::python-host-encoding-http-context'
CLOUD = 'micro-behaviors/communications/http/services/cloud::multi-cloud-credential-endpoint-context'
RETIRED = {
    'objectives/exfiltration/stealer/system-info/identity::python-system-info-exfil',
    'objectives/credential-access/ssh/key::python-ssh-harvest-exfil',
    'objectives/credential-access/ssh/key::python-ssh-directory-enumeration',
    'objectives/credential-access/ssh/key::python-expanduser-ssh-directory-enumeration',
    'micro-behaviors/os/env/secret-name::python-environ-items-credential-filter',
    'micro-behaviors/os/env/secret-name::python-environ-loop-credential-filter',
}


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        doc, end = decoder.raw_decode(text)
        yield doc
        text = text[end:]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cleave', default=str(ROOT.parent / 'cleave/target/release/cleave'))
    p.add_argument('--sample-root', type=Path)
    args = p.parse_args()
    cases = []
    with tempfile.TemporaryDirectory(prefix='litellm-improve-controls-') as temp:
        work = Path(temp)

        def add(name, source, required=(), forbidden=(), no_hostile=True):
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source)
            cases.append((name, path, set(required), set(forbidden), no_hostile))

        cng = 'import ctypes\nbcrypt = ctypes.windll.bcrypt\nbcrypt.BCryptOpenAlgorithmProvider()\nbcrypt.BCryptEncrypt()\n'
        add('cng.py', cng, forbidden=[BCRYPT, BCRYPT_REF, BCRYPT_API])
        add('password.py', 'import bcrypt\nbcrypt.hashpw(password, bcrypt.gensalt())\n', [BCRYPT_API])
        add('password-alias.py', 'from bcrypt import hashpw as hash_password\nhash_password(password, salt)\n', ['metadata/import/python/bcrypt::bcrypt'])
        add('mixed-crypto.py', cng + 'from bcrypt import checkpw\ncheckpw(password, digest)\n', ['metadata/import/python/bcrypt::bcrypt'])
        add('bcrypt.go', 'package main\nimport "golang.org/x/crypto/bcrypt"\nfunc main() {}\n', [BCRYPT_REF])
        add('bcrypt.js', 'const bcrypt = require("bcrypt");\nbcrypt.hash(password, 10);\n', [BCRYPT_REF])
        add('bcrypt.rb', 'require "bcrypt"\nhash = BCrypt::Password.create(password)\n', [BCRYPT_REF])
        add('cng-dll.js', 'const provider = "bcrypt.dll";\n', forbidden=[BCRYPT, BCRYPT_REF, BCRYPT_API])

        for api in ('findfirst', 'findnext'):
            add(api + '.c', 'void inspect(void) { ' + api + '(path, data); }\n',
                ['micro-behaviors/fs/directory/readdir::crt-directory-enumeration'])

        imports = 'from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes\n'
        add('cbc.py', imports + 'x = Cipher(algorithms.AES(key), modes.CBC(iv))\n', [AES])
        add('cbc-alias.py', 'from cryptography.hazmat.primitives.ciphers import Cipher as C, algorithms as a, modes as m\nx = C(a.AES(key), m.CBC(iv))\n', [AES])
        add('gcm.py', imports + 'x = Cipher(algorithms.AES(key), modes.GCM(iv))\n', forbidden=[AES])
        add('non-aes-cbc.py', imports + 'x = Cipher(algorithms.Camellia(key), modes.CBC(iv))\n', forbidden=[AES])
        add('split-ciphers.py', imports + 'x = Cipher(algorithms.AES(key), modes.GCM(iv))\ny = Cipher(algorithms.Camellia(key), modes.CBC(iv))\n', forbidden=[AES])

        add('env-selected.py', 'import os\nx = {k:v for k,v in os.environ.items() if "TOKEN" in k.upper()}\n', [ENV])
        add('env-renamed.py', 'import os\nx = {label:data for label,data in os.environ.items() if "password" in label.lower()}\n', [ENV])
        add('env-key-loop.py', 'import os\nfor key in os.environ:\n    if "SECRET" in key:\n        selected[key] = os.environ[key]\n', [ENV])
        add('env-suffix.py', 'import os\nfor key,value in os.environ.items():\n    if key.endswith(("_TOKEN", "_KEY")):\n        selected[key] = value\n', [ENV])
        add('env-any-inline.py', 'import os\nx = {k:v for k,v in os.environ.items() if any(s in k for s in ("TOKEN", "KEY", "SECRET"))}\n', [ENV])
        add('env-any-list.py', 'import os\ndef collect():\n    patterns = ["API_KEY", "SECRET", "TOKEN", "PASSWORD"]\n    for key,value in os.environ.items():\n        if any(term in key.upper() for term in patterns):\n            selected[key] = value\n', [ENV])
        add('env-any-unrelated.py', 'import os\nx = {k:v for k,v in os.environ.items() if any(s in other for s in ("TOKEN", "KEY"))}\n', forbidden=[ENV])
        add('env-any-negated.py', 'import os\nx = {k:v for k,v in os.environ.items() if not any(s in k for s in ("TOKEN", "KEY"))}\n', forbidden=[ENV])
        for name, code in [
            ('truthy', 'x = [{"name":k,"value":v} for k,v in os.environ.items() if v]\nURL = "TOKEN"\n'),
            ('unrelated-condition', 'x = {k:v for k,v in os.environ.items() if "TOKEN" in other}\n'),
            ('value-condition', 'x = {k:v for k,v in os.environ.items() if "TOKEN" in v}\n'),
            ('exclude', 'x = {k:v for k,v in os.environ.items() if k != "API_TOKEN"}\n'),
            ('not-in', 'x = {k:v for k,v in os.environ.items() if "SECRET" not in k}\n'),
            ('negated', 'x = {k:v for k,v in os.environ.items() if not k.endswith("_TOKEN")}\n'),
            ('namespace', 'x = {k:v for k,v in os.environ.items() if k.startswith("MYAPP_")}\n'),
        ]:
            add('env-' + name + '.py', 'import os\n' + code, forbidden=[ENV])

        add('host-diagnostics.py', 'import getpass, socket, base64, urllib.request\nuser = getpass.getuser()\nhost = socket.gethostname()\nencoded = base64.b64encode(host.encode())\nreq = urllib.request.Request("https://example.org/status")\n', [HOST])
        add('ssh-inventory-status.py', 'import os, requests\nfiles = os.listdir(os.path.expanduser("~/.ssh"))\nrequests.post("https://example.org/status", json={"ok": True})\n', [SSH])
        add('cloud-reference.py', 'import urllib.request\naws = "http://169.254.169.254/latest/meta-data/iam/security-credentials/"\nazure = "http://169.254.169.254/metadata/instance"\n', [CLOUD])
        add('single-cloud.py', 'import urllib.request\naws = "http://169.254.169.254/latest/meta-data/iam/security-credentials/"\n', forbidden=[CLOUD])

        sql_creds = 'micro-behaviors/data/db/sql::litellm-credentials-from-clause'
        sql_models = 'micro-behaviors/data/db/sql::litellm-models-from-clause'
        add('sql-text.py', 'child = \'query("SELECT credential_values FROM LiteLLM_CredentialsTable"); query("SELECT litellm_params FROM LiteLLM_ProxyModelTable")\'\n', [sql_creds, sql_models])
        add('schema-names.py', 'names = ["LiteLLM_CredentialsTable", "LiteLLM_ProxyModelTable"]\n', forbidden=[sql_creds, sql_models])

        if args.sample_root:
            for variant in ('unix', 'windows'):
                for name in ('cook.py', 'sitecustomize.py', 'cook.pth'):
                    path = args.sample_root / 'wheel-payloads' / variant / name
                    cases.append((variant + '/' + name, path,
                                  {AES, sql_creds, sql_models} if name.endswith('.py') else set(),
                                  {BCRYPT, BCRYPT_REF, BCRYPT_API, ENV}, False))
            # Mutate inert source to check detection without campaign names or
            # callback spellings. These generated programs are never executed.
            collector = (args.sample_root / 'decoded/cook-decoded.py').read_text()
            collector = collector.replace('privcollect', 'telemetry_copy').replace('PRIVCOLLECT', 'TELEMETRY_COPY')
            collector = collector.replace('www.litellm.dev', 'sink.example.org').replace('pc_', 'helper_').replace('PC_', 'DATA_')
            packed = base64.b64encode(zlib.compress(collector.encode())).decode()
            add('variant-collector.py', 'import base64, zlib\nexec(zlib.decompress(base64.b64decode(' + repr(packed) + ')))\n',
                [AES, 'objectives/credential-access/browser/chromium::python-dpapi-chromium-login-decrypt',
                 'objectives/exfiltration/stealer/dev-secret::encoded-multi-developer-secret-exfil'],
                ['well-known/malware/stealer/privcollect::privcollect-tool-marker',
                 'objectives/command-and-control/infrastructure/domain/known::litellm-dev-host-reference'], False)

            startup = (args.sample_root / 'wheel-payloads/unix/sitecustomize.py').read_text()
            functions = [node.name for node in ast.parse(startup).body
                         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
            rename = {name: 'callback_' + str(i) for i, name in enumerate(functions)}
            tokens = []
            previous = None
            for token in tokenize.generate_tokens(io.StringIO(startup).readline):
                if token.type == tokenize.NAME and token.string in rename and previous != '.':
                    token = token._replace(string=rename[token.string])
                tokens.append(token)
                if token.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT):
                    previous = token.string
            startup = tokenize.untokenize(tokens).replace('letters9813/pythonclient-test', 'example/testing')
            add('variant/sitecustomize.py', startup,
                ['objectives/command-and-control/remote-command/http-poll::python-threadpool-http-exec-daemon',
                 'objectives/persistence/system/python-startup::startup-hook-threadpool-code-daemon'],
                [BCRYPT, BCRYPT_REF, BCRYPT_API, ENV], False)

            for name in ('cook-decoded.py', 'sitecustomize-decoded.py'):
                path = args.sample_root / 'decoded' / name
                cases.append((name, path, {AES, sql_creds, sql_models}, {BCRYPT, BCRYPT_REF, BCRYPT_API, ENV}, False))

        env = dict(os.environ, CLEAVE_NO_UPDATE_CHECK='1')
        run = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json',
                              'analyze', *(str(row[1]) for row in cases)],
                             env=env, capture_output=True, text=True, check=True)
        reports = list(documents(run.stdout))
        files = [file for report in reports for file in report.get('files', [])]
        for name, path, required, forbidden, no_hostile in cases:
            analyzed = [file for file in files if file['path'] == str(path)
                        or file['path'].startswith(str(path) + '##')]
            assert analyzed, (name, 'not analyzed')
            traits = [t for file in analyzed for t in file.get('traits', [])]
            ids = {t['id'] for t in traits}
            assert required <= ids, (name, 'missing', sorted(required - ids))
            assert not (forbidden | RETIRED) & ids, (name, 'unexpected', sorted((forbidden | RETIRED) & ids))
            if no_hostile:
                assert not [t['id'] for t in traits if t.get('crit', 0) >= 5], (name, 'unexpected hostile', [t['id'] for t in traits if t.get('crit', 0) >= 5])
            print('PASS', name)
        print(len(cases), 'focused controls passed')


if __name__ == '__main__':
    main()
