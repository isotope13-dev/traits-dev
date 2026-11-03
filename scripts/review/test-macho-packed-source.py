#!/usr/bin/env python3
"""Check source coverage for the paired Mach-O loader API clusters."""
import json
import pathlib
import subprocess
import tempfile

source = '''
const char *symbols[] = {
  "JustInTimeLoader4make", "analyzeSegmentsLayout", "applyFixups",
  "runInitializersBottomUpPlusUpwardLinks", "NSCreateObjectFileImageFromMemory",
  "NSLinkModule", "NSLookupSymbolInModule", "aP_depack_safe"
};
int flags = MAP_JIT;
'''
cases = {
    'paired-loader': (source, True),
    'no-depacker': (source.replace('aP_depack_safe', 'ordinary_decoder'), False),
    'no-jit': (source.replace('MAP_JIT', 'MAP_PRIVATE'), False),
    'no-dyld4': (source.replace('JustInTimeLoader4make', 'other_loader'), False),
    'no-legacy': (source.replace('NSLinkModule', 'other_linker'), False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (content, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.c')
        path.write_text(content)
        data = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::packed-macho-memory-loader-source') for t in data['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('Mach-O loader source observation boundaries passed.')
