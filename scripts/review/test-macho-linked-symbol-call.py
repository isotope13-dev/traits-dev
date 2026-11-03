#!/usr/bin/env python3
"""Check the data bindings in memory-module symbol invocation."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
atom = 'micro-behaviors/process/deploy/module-load::macho-linked-module-symbol-call'
hostile = 'objectives/execution/payload/image-map::packed-macho-linked-symbol-execution'
source = '''
const char *metadata = "JustInTimeLoader4make analyzeSegmentsLayout applyFixups runInitializersBottomUpPlusUpwardLinks aP_depack_safe MAP_JIT";
void run(void *buffer, unsigned long size, char *name) {
  void *image = 0;
  int result = NSCreateObjectFileImageFromMemory_func(buffer, size, &image);
  void *module = NSLinkModule_func(image, "memory", 4);
  void *symbol = NSLookupSymbolInModule_func(module, name);
  void *address = NSAddressOfSymbol_func(symbol);
  void (*entry)(void) = (void (*)(void))address;
  entry();
}
'''
cases = {
    'complete': (source, True, True),
    'other-image': (source.replace('NSLinkModule_func(image,', 'NSLinkModule_func(other,'), False, False),
    'other-module': (source.replace('NSLookupSymbolInModule_func(module,', 'NSLookupSymbolInModule_func(other,'), False, False),
    'other-symbol': (source.replace('NSAddressOfSymbol_func(symbol)', 'NSAddressOfSymbol_func(other)'), False, False),
    'other-address': (source.replace('))address;', '))other;'), False, False),
    'other-call': (source.replace('  entry();', '  other();'), False, False),
    'lookalike': (source.replace('NSLinkModule_func(image,', 'NSLinkModuleFake(image,'), False, False),
    'without-jit': (source.replace('MAP_JIT', 'OTHER_FLAG'), True, False),
}
with tempfile.TemporaryDirectory(prefix='macho-symbol-call-') as tmp:
    paths = []
    for name, (content, _, _) in cases.items():
        path = Path(tmp) / (name + '.c')
        path.write_text(content)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        ids = {t['id'] for t in report.get('traits', [])}
        assert (atom in ids, hostile in ids) == cases[name][1:], (name, atom in ids, hostile in ids)
print('Mach-O linked symbol call boundaries passed.')
