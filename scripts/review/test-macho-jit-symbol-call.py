#!/usr/bin/env python3
"""The JIT allocation, resolver input, and indirect call must share paths."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
ATOM = 'micro-behaviors/process/deploy/module-load::macho-jit-resolved-symbol-call'
HOSTILE = 'objectives/execution/payload/image-map::packed-macho-jit-resolved-symbol-execution'
SOURCE = '''
const char *apis = "JustInTimeLoader4make analyzeSegmentsLayout applyFixups runInitializersBottomUpPlusUpwardLinks aP_depack_safe NSCreateObjectFileImageFromMemory NSLinkModule NSLookupSymbolInModule";
void run(char *name, unsigned long size) {
  void *mapped = syscall_mmap(0, size, PROT_READ, MAP_PRIVATE | MAP_ANON | MAP_JIT, -1, 0);
  uintptr_t image = (uintptr_t)mapped;
  void *address = find_symbol((uint64_t)image, name, 0);
  void (*entry)(void) = (void (*)(void))address;
  entry();
}
'''
CASES = {
    'complete': (SOURCE, True, True),
    'other-allocation': (SOURCE.replace('(uintptr_t)mapped', '(uintptr_t)other'), False, False),
    'other-image': (SOURCE.replace('(uint64_t)image', '(uint64_t)other'), False, False),
    'other-address': (SOURCE.replace('))address;', '))other;'), False, False),
    'other-call': (SOURCE.replace('  entry();', '  other();'), False, False),
    'no-jit': (SOURCE.replace(' | MAP_JIT', ' | MAP_OTHER'), False, False),
    'string-jit': (SOURCE.replace('MAP_PRIVATE | MAP_ANON | MAP_JIT', '"MAP_JIT"'), False, False),
    'other-resolver': (SOURCE.replace('find_symbol(', 'unrelated('), False, False),
    'no-loader-cluster': (SOURCE.replace('JustInTimeLoader4make', 'unrelated'), True, False),
}
with tempfile.TemporaryDirectory(prefix='macho-jit-call-') as tmp:
    paths = []
    for name, (source, _, _) in CASES.items():
        path = Path(tmp) / (name + '.c')
        path.write_text(source)
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        ids = {trait['id'] for trait in report.get('traits', [])}
        found = (ATOM in ids, HOSTILE in ids)
        assert found == CASES[name][1:], (name, found, CASES[name][1:])
print('JIT mapping and resolved-call observations require matching bindings')
