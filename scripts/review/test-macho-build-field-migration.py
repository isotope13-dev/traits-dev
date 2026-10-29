#!/usr/bin/env python3
"""Exercise embedded Mach-O build fields and their exact suppression.

Requires macOS clang, the Apple linker, and the sibling Cleave release binary.
Compiled fixtures are analyzed, never executed.
"""
from pathlib import Path
import plistlib
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
XCODE = 'metadata/binary/bundle::macho-info-plist-dtxcode'
PLATFORM = 'metadata/binary/bundle::macho-info-plist-dtplatformbuild'
REFERENCE = 'metadata/build/toolchain::dtxcode-text-reference'
CONSUMER = 'well-known/dual-use/access-control/imyfone::suspicious-qt-plist-legacy-qmake'

with tempfile.TemporaryDirectory(prefix='macho-build-fields-') as temp:
    work = Path(temp)
    source = work / 'main.c'
    source.write_text('int main(void) { return 0; }\n')
    assembly = work / 'markers.s'
    assembly.write_text('.section __TEXT,__text,regular,pure_instructions\n'
                        '.globl _fixture_markers\n_fixture_markers:\n'
                        '.asciz "org.qt-project.QtCore"\n'
                        '.asciz "Created by Qt/QMake"\n'
                        '.asciz "<string>5.6.3</string>"\n'
                        '.asciz "DTXcode"\n')
    cases = (
        ('xcode', {'DTXcode': '1540'}, True, False),
        ('platform', {'DTPlatformBuild': '23A344'}, False, True),
        ('both', {'DTXcode': '1540', 'DTPlatformBuild': '23A344'}, True, True),
        ('unrelated', {'Other': 'DTXcode', 'Number': '1234', 'Version': '3.5'}, False, False),
    )
    for name, values, has_xcode, has_platform in cases:
        plist, binary = work / (name + '.plist'), work / name
        plist.write_bytes(plistlib.dumps(values))
        subprocess.run(['clang', str(source), str(assembly),
                        '-Wl,-sectcreate,__TEXT,__info_plist,' + str(plist),
                        '-o', str(binary)], check=True)
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(ROOT), 'test-rules',
                                 '--rules', ','.join((XCODE, PLATFORM, REFERENCE, CONSUMER)),
                                 str(binary)], check=True, capture_output=True, text=True)
        for rule, expected in ((XCODE, has_xcode), (PLATFORM, has_platform),
                               (REFERENCE, True), (CONSUMER, not (has_xcode or has_platform))):
            status = 'MATCHED ' if expected else 'NOT MATCHED '
            if '\n' + status + rule + ' ' not in result.stdout:
                raise SystemExit(f'{name}: unexpected result for {rule}\n{result.stdout}\n{result.stderr}')
        print(f'{name}: ok', flush=True)
