#!/usr/bin/env python3
"""Static regression checks for file rewriting, local loaders and FD passing.

Generates source controls and inspects trait IDs. Never compiles or executes
sample code. Run with --work-dir pointing outside the trait checkout.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STREAM = 'micro-behaviors/fs/write/encrypted::cpp-file-stream-cipher-rewrite'
LOCKER = 'objectives/impact/ransom/encrypt/native-locker::stream-cipher-inplace-note-locker'
THREAD = 'objectives/execution/payload/native-call::copied-executable-buffer-local-thread'
HANDOFF = 'micro-behaviors/communications/socket/handoff::scm-rights-message-send-source'
ROOTCALL = 'micro-behaviors/process/identity/setuid::setid-root-call-source'
OVS = 'objectives/privilege-escalation/exploit/kernel::ovs-pagecache-root-shell-exploit-scaffold'
IDENTITY = 'well-known/tool/offensive/payload-corpus::seclists-corpus-documentation'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default=str(ROOT.parent / 'cleave/target/release/cleave'))
    parser.add_argument('--traits-dir', type=Path, default=ROOT)
    parser.add_argument('--work-dir', type=Path, required=True)
    args = parser.parse_args()
    work = args.work_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    cases = []

    def add(name, source, required=(), forbidden=(), suffix='.c'):
        path = work / 'inputs' / (name + suffix)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
        cases.append(dict(name=name, path=path, required=set(required), forbidden=set(forbidden)))

    locker = (ROOT / 'testdata/hostile/controls/six-source-improve/locker.cpp').read_text()
    add('locker-helpers-unreached', locker, [STREAM, LOCKER], suffix='.cpp')
    add('locker-renamed', locker.replace('plaintext', 'input_bytes').replace('ciphertext', 'output_bytes')
        .replace('file.', 'document.').replace('file(path', 'document(path')
        .replace('encrypt_file', 'transform').replace('.sealed', '.changed'),
        [STREAM, LOCKER], suffix='.cpp')
    add('locker-xsalsa', locker.replace('chacha20_ietf', 'xsalsa20'), [STREAM, LOCKER], suffix='.cpp')
    add('locker-no-nonce-call', locker.replace('    randombytes_buf(nonce.data(), nonce.size());\n', ''),
        [STREAM, LOCKER], suffix='.cpp')
    add('locker-comments', locker.replace('    file.seekp(offset);', '    /* write result */\n    file.seekp(offset);'),
        [STREAM, LOCKER], suffix='.cpp')
    direct = locker.replace('for (std::size_t index = 0; index < rounds; ++index) {',
        'const std::size_t index = 0;').replace('\n  }\n\n  // The shared nonce', '\n\n  // The shared nonce')
    add('locker-direct-routine', direct, [STREAM, LOCKER], suffix='.cpp')
    vector = locker.replace('#include <string>', '#include <string>\n#include <vector>')
    vector = vector.replace('std::string plaintext', 'std::vector<unsigned char> plaintext')
    vector = vector.replace('std::string ciphertext', 'std::vector<unsigned char> ciphertext')
    vector = vector.replace('file.read(plaintext.data()', 'file.read(reinterpret_cast<char *>(plaintext.data())')
    vector = vector.replace('file.write(ciphertext.data()',
        'file.write(reinterpret_cast<const char *>(ciphertext.data())')
    vector = vector.replace('reinterpret_cast<unsigned char *>(ciphertext.data())', 'ciphertext.data()')
    vector = vector.replace('reinterpret_cast<const unsigned char *>(plaintext.data())', 'plaintext.data()')
    add('locker-byte-vector', vector, [STREAM, LOCKER], suffix='.cpp')
    no_locals = locker
    for statement in ['const std::size_t offset = quarter * index;',
                      'const std::size_t length = std::min(kChunkLimit, file_size - offset);',
                      "std::string plaintext(length, '\\0');", "std::string ciphertext(length, '\\0');"]:
        no_locals = no_locals.replace('    ' + statement + '\n', '')
    no_locals = no_locals.replace('  for (std::size_t index',
        "  const std::size_t offset = 0, length = 16;\n  std::string plaintext(length, '\\0');\n"
        "  std::string ciphertext(length, '\\0');\n  for (std::size_t index")
    add('locker-buffers-outside-loop', no_locals, [STREAM, LOCKER], suffix='.cpp')
    add('ordinary-file-encryption', locker.replace('Your files were encrypted. Follow the payment instructions.',
        'Backup encrypted successfully.'), [STREAM], [LOCKER], '.cpp')
    add('locker-plaintext-written', locker.replace('file.write(ciphertext.data()', 'file.write(plaintext.data()'),
        forbidden=[STREAM, LOCKER], suffix='.cpp')
    add('locker-different-input', locker.replace('const unsigned char *>(plaintext.data())',
        'const unsigned char *>(unrelated.data())'), forbidden=[STREAM, LOCKER], suffix='.cpp')
    add('locker-different-stream', locker.replace('file.seekp(offset);', 'other.seekp(offset);')
        .replace('file.write(ciphertext.data()', 'other.write(ciphertext.data()'),
        forbidden=[STREAM, LOCKER], suffix='.cpp')
    add('locker-memory-stream', locker.replace('std::fstream file(', 'std::stringstream file('),
        forbidden=[STREAM, LOCKER], suffix='.cpp')
    add('locker-shadowed-file-stream', locker.replace('    const std::size_t offset',
        '    std::stringstream file;\n    const std::size_t offset'),
        forbidden=[STREAM, LOCKER], suffix='.cpp')
    add('locker-shadowed-file-stream-after-declarations', locker.replace('    file.seekg(offset);',
        '    std::stringstream file;\n    file.seekg(offset);'),
        forbidden=[STREAM, LOCKER], suffix='.cpp')
    add('locker-note-and-prototype', locker[:locker.index('void encrypt_file(')] +
        '\nconst char *notice = "Your files were encrypted. Follow the payment instructions.";\n',
        forbidden=[STREAM, LOCKER], suffix='.cpp')

    loader = (ROOT / 'testdata/suspicious/controls/six-source-improve/cryptoapi-loader.c').read_text()
    add('cryptoapi-loader', loader, [THREAD])
    add('loader-renamed', re.sub(r'\bmemory\b', 'region', loader), [THREAD])
    add('loader-symbolic-protection', loader.replace('0x40', 'PAGE_EXECUTE_READWRITE'), [THREAD])
    add('loader-decimal-protection', loader.replace('0x40', '32'), [THREAD])
    add('loader-no-null-guard', loader.replace('    if (!memory) return 7;\n', ''), [THREAD])
    add('loader-comments', loader.replace('    HANDLE thread', '    /* start copied bytes */\n    HANDLE thread'), [THREAD])
    add('loader-readwrite', loader.replace('0x40', 'PAGE_READWRITE'), forbidden=[THREAD])
    add('loader-other-copy-target', loader.replace('memcpy(memory,', 'memcpy(other,'), forbidden=[THREAD])
    add('loader-other-entry', loader.replace('(LPTHREAD_START_ROUTINE)memory', 'worker'), forbidden=[THREAD])
    add('loader-context-only', loader.replace('(LPTHREAD_START_ROUTINE)memory, NULL', 'worker, memory'),
        forbidden=[THREAD])
    add('loader-reassigned-entry', loader.replace('    HANDLE thread', '    memory = other;\n    HANDLE thread'),
        forbidden=[THREAD])
    add('loader-decoy-executable-allocation', loader.replace('0x40', 'PAGE_READWRITE').replace(
        '    memcpy(memory,', '    VirtualAlloc(NULL, length, 0x3000, 0x40);\n    memcpy(memory,'), forbidden=[THREAD])
    add('loader-comment-only', ''.join('// ' + line for line in loader.splitlines(keepends=True)),
        forbidden=[THREAD])

    handoff = '''#include <sys/socket.h>
#include <string.h>
int transfer(int channel, int fd) {
    struct msghdr message = {0};
    char ancillary[CMSG_SPACE(sizeof(int))];
    message.msg_control = ancillary;
    message.msg_controllen = sizeof(ancillary);
    struct cmsghdr *header = CMSG_FIRSTHDR(&message);
    header->cmsg_level = SOL_SOCKET;
    header->cmsg_type = SCM_RIGHTS;
    header->cmsg_len = CMSG_LEN(sizeof(int));
    memcpy(CMSG_DATA(header), &fd, sizeof(int));
    return sendmsg(channel, &message, 0);
}
'''
    add('fd-handoff', handoff, [HANDOFF])
    add('fd-handoff-renamed', handoff.replace('message', 'packet').replace('header', 'control'), [HANDOFF])
    add('fd-handoff-comments', handoff.replace('    memcpy', '    /* copy descriptor */\n    memcpy'), [HANDOFF])
    add('fd-other-message', handoff.replace('sendmsg(channel, &message', 'sendmsg(channel, &other'), forbidden=[HANDOFF])
    add('fd-other-header', handoff.replace('CMSG_DATA(header)', 'CMSG_DATA(other)'), forbidden=[HANDOFF])
    add('fd-other-control-type', handoff.replace('SCM_RIGHTS', 'SCM_CREDENTIALS'), forbidden=[HANDOFF])
    add('fd-comment-only', '/*\n' + handoff + '\n*/\n', forbidden=[HANDOFF])

    add('root-id-call', '#include <unistd.h>\nvoid root(void) { setuid(0); }\n', [ROOTCALL])
    add('root-id-comment', '#include <unistd.h>\n/* setuid(0); */\n', forbidden=[ROOTCALL])
    add('root-id-string', 'const char *text = "setuid(0)";\n', forbidden=[ROOTCALL])
    ovs = (ROOT / 'testdata/hostile/controls/six-source-improve/ovs-scaffold.c').read_text()
    add('ovs-root-shell-scaffold', ovs, [OVS], [ROOTCALL])
    no_payload, replaced = re.subn(r'static const uint8_t root_payload\[\].*?\};',
        'static const uint8_t root_payload[] = {0};', ovs, count=1, flags=re.S)
    assert replaced == 1, 'OVS fixture must contain exactly one payload array'
    add('ovs-without-payload', no_payload, forbidden=[OVS])
    identity = "SecLists is the security tester's companion. It's a collection of multiple types of lists used during security assessments"
    add('seclists-documentation', identity, [IDENTITY], suffix='.md')
    add('seclists-reference', 'This document links to SecLists as an example.', forbidden=[IDENTITY], suffix='.md')

    env = os.environ.copy()
    env.update(CLEAVE_CACHE_DIR=str(work / 'cache'), CLEAVE_NO_UPDATE_CHECK='1',
               CLEAVE_RAYON_THREADS='4', RAYON_NUM_THREADS='4')
    result = subprocess.run([args.cleave, '--traits-dir', str(args.traits_dir.resolve()),
        '--json', *[str(c['path']) for c in cases]], env=env, text=True, capture_output=True)
    (work / 'report.jsonl').write_text(result.stdout)
    (work / 'scan.log').write_text(result.stderr)
    if result.returncode not in (0, 1):
        raise SystemExit(f'cleave failed ({result.returncode}); see {work / "scan.log"}')
    observations = {}
    for line in result.stdout.splitlines():
        report = json.loads(line)
        for file in report.get('raw', report).get('files', []):
            observations[str(Path(file['path']).resolve())] = {t['id'] for t in file.get('traits', [])}
    failures = []
    retired = {
        'objectives/command-and-control/dropper/staging/memory::encoded-capi-executable-memory-staging-source',
        'objectives/evasion/process/injection/native::capi-decrypt-executable-thread-source',
    }
    for case in cases:
        found = observations.get(str(case['path']))
        if found is None:
            failures.append(f'{case["name"]}: missing report')
            continue
        missing = case['required'] - found
        unexpected = (case['forbidden'] | retired) & found
        if missing or unexpected:
            failures.append(f'{case["name"]}: missing={sorted(missing)} unexpected={sorted(unexpected)}')
    summary = dict(cases=len(cases), passed=len(cases) - len(failures), failures=failures)
    (work / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    main()
