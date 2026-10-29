#!/usr/bin/env python3
"""A benign Acrobat API reference is recognizable without an exploit claim."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULES = ('metadata/document/pdf/script::pdf-acrobat-api-reference',
         'objectives/execution/interpreter/eval/document::pdf-js-acrobat-api-reference')


def pdf(script):
    code = script.encode()
    objects = [b'<< /Type /Catalog /Pages 2 0 R /OpenAction 4 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>',
               b'<< /S /JavaScript /JS 5 0 R >>',
               b'<< /Length ' + str(len(code)).encode() + b' >>\nstream\n' + code + b'\nendstream']
    out = bytearray(b'%PDF-1.4\n%' + b'P' * 600 + b'\n')
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out.extend(f'{index} 0 obj\n'.encode() + obj + b'\nendobj\n')
    xref = len(out)
    out.extend(f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]:
        out.extend(f'{offset:010d} 00000 n \n'.encode())
    out.extend(f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    return out


with tempfile.TemporaryDirectory(prefix='acrobat-api-probe-') as directory:
    for name, code, expected in [('api', "Collab.getIcon('example');", True),
                                  ('other', "Collab.getText('example');", False)]:
        target = Path(directory) / (name + '.pdf')
        target.write_bytes(pdf(code))
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules',
                                 str(target), '--rules', ','.join(RULES)], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        for rule in RULES:
            prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), result.stdout
        print(name + ': passed', flush=True)
