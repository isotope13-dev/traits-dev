"""Build inert ELF controls and scan them; never execute them.

Usage: python3 testdata/triage/youtube-drive-agent/verify.py /tmp/agent-controls
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RESOLVER = 'objectives/command-and-control/infrastructure/dead-drop::'
YOUTUBE = RESOLVER + 'youtube-comment-agent-c2-resolver'
DRIVE = RESOLVER + 'drive-text-agent-c2-resolver'
CLEANUP = 'objectives/evasion/indicator-removal/cleanup::dead-drop-agent-live-file-removal'
EXEC = 'objectives/command-and-control/backdoor/control/rmm::dead-drop-agent-detached-execution'
TARGETS = {YOUTUBE, DRIVE, CLEANUP, EXEC}

STRINGS = {
    'youtube': 'https://www.googleapis.com/youtube/v3/commentThreads?videoId=CHANGED',
    'field': '"textOriginal"',
    'youtube_resolution': 'Domain obtained from YouTube',
    'drive': 'https://drive.usercontent.google.com/download?id=CHANGED&export=download',
    'drive_resolution': 'Domain obtained from Google Drive text file',
    'c2': 'Failed to read C2 text file',
    'config': 'Domain injected into replacement.conf',
    'cleanup': 'Agent files deleted, monitoring for liveness',
}


def elf(strings, syscalls):
    # Valid sectionless ELF: RET entry, unreachable syscall wrappers, data.
    # None of these fixture bytes are launched as a program.
    code = b'\xc3' + b''.join(b'\xb8' + struct.pack('<I', n) + b'\x0f\x05\xc3'
                            for n in syscalls)
    payload = code.ljust(0x100, b'\x90') + '\0'.join(strings).encode() + b'\0'
    size = 0x1000 + len(payload)
    header = struct.pack('<16sHHIQQQIHHHHHH', b'\x7fELF\x02\x01\x01' + b'\0'*9,
                         2, 62, 1, 0x401000, 64, 0, 0, 64, 56, 1, 64, 0, 0)
    segment = struct.pack('<IIQQQQQQ', 1, 5, 0, 0x400000, 0x400000, size, size, 0x1000)
    return (header + segment).ljust(0x1000, b'\0') + payload


def main():
    dest = Path(sys.argv[1]).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    full = set(STRINGS)
    cases = {
        'both-sources': (full, [59, 87, 112], TARGETS),
        'youtube-only': (full - {'drive', 'drive_resolution'}, [59, 87, 112],
                         {YOUTUBE, CLEANUP, EXEC}),
        'drive-only': (full - {'youtube', 'field', 'youtube_resolution'}, [59, 87, 112],
                       {DRIVE, CLEANUP, EXEC}),
        'api-references-only': ({'youtube', 'field', 'drive'}, [59, 87, 112], set()),
        'no-config-injection': (full - {'config'}, [59, 87, 112], set()),
        'no-c2-diagnostic': (full - {'c2'}, [59, 87, 112], set()),
        'no-live-deletion': (full - {'cleanup'}, [59, 87, 112], {YOUTUBE}),
        'no-unlink': (full, [59, 112], {YOUTUBE, DRIVE}),
        'no-execution': (full, [87, 112], {YOUTUBE, DRIVE, CLEANUP}),
        'no-detachment': (full, [59, 87], {YOUTUBE, DRIVE, CLEANUP}),
        'ordinary-agent-cleanup': ({'cleanup', 'config'}, [59, 87, 112], set()),
        'youtube-no-field': (full - {'field', 'drive', 'drive_resolution'},
                             [59, 87, 112], set()),
        'youtube-no-resolution': (full - {'youtube_resolution', 'drive', 'drive_resolution'},
                                  [59, 87, 112], set()),
        'drive-no-endpoint': (full - {'drive', 'youtube', 'field', 'youtube_resolution'},
                              [59, 87, 112], set()),
    }
    expected = {}
    for name, (keys, calls, matches) in cases.items():
        path = dest / (name + '.elf')
        path.write_bytes(elf([STRINGS[k] for k in sorted(keys)], calls))
        expected[path.name] = matches
    # Renamed files, endpoints/IDs, and equivalent diagnostic wording must
    # preserve the observation; the loader's original IOC strings are absent.
    variant = list(STRINGS.values())
    variant = [s.replace('obtained', 'resolved').replace('deleted, monitoring', 'unlinked, checking')
               for s in variant]
    path = dest / 'renamed-and-reworded.elf'
    path.write_bytes(elf(variant, [59, 87, 112]))
    expected[path.name] = TARGETS
    env = {**os.environ, 'CLEAVE_VALIDATE': '0', 'CLEAVE_NO_UPDATE_CHECK': '1'}
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'json', str(dest)], env=env, check=True,
                            stdout=subprocess.PIPE)
    seen = set()
    # Some installed Cleave builds concatenate directory JSON envelopes
    # without newlines, so decode each complete object from the stream.
    decoder = json.JSONDecoder()
    remaining = result.stdout.decode().lstrip()
    files = []
    while remaining:
        report, end = decoder.raw_decode(remaining)
        files.extend(report['files'])
        remaining = remaining[end:].lstrip()
    for item in files:
        name = Path(item['path']).name
        if name not in expected:
            continue
        hostile = {t['id'] for t in item['traits'] if t['crit'] == 5}
        assert hostile == expected[name], (name, sorted(hostile), sorted(expected[name]))
        seen.add(name)
        print('PASS', name, len(hostile), 'hostile findings')
    assert seen == set(expected), ('missing cases', set(expected) - seen)


if __name__ == '__main__':
    main()
