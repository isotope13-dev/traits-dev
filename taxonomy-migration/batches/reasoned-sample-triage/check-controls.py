"""Assert distinguishing evidence in atomscan JSON; no fixture is executed."""
import json, sys

files = json.load(open(sys.argv[1]))['raw']['files']
by_name = {f['path'].split('!!')[-1]: {t['id']: t['crit'] for t in f['traits']} for f in files}
concat = 'micro-behaviors/data/string/concat::lua-double-indexed-concat-loop'
escaped = 'metadata/lang/encoding::lua-many-decimal-escaped-strings'
concealment = 'objectives/anti-static/obfuscation/string/encoding::lua-escaped-indexed-string-reassembly'
resolver = 'micro-behaviors/os/api-resolution/manual::peb-export-resolver-x64'
hashing = 'objectives/anti-static/obfuscation/imports/api-hashing::export-walk-with-hash-arithmetic'
decoded = 'objectives/anti-static/obfuscation/payload/encoded/exec::decoded-function-constructor-argument'
checks = {
    'indexed-escaped.lua': ({concat: 3, escaped: 3, concealment: 4}, []),
    'escaped-no-loop.lua': ({escaped: 3}, [concat, concealment]),
    'ordinary-loop.lua': ({}, [concat, escaped, concealment]),
    'peb-export.exe': ({resolver: 3, hashing: 4}, []),
    'peb-header-only.exe': ({}, [resolver, hashing]),
    'wrong-arch.exe': ({}, [resolver, hashing]),
    'decoded-code.js': ({decoded: 4}, []),
    'obfuscated-ui.js': ({}, [decoded]),
}
for name, (positive, negative) in checks.items():
    actual = by_name[name]
    for trait, severity in positive.items():
        assert actual.get(trait) == severity, (name, trait, actual.get(trait))
    for trait in negative:
        assert trait not in actual, (name, trait)
    if name == 'obfuscated-ui.js':
        assert all(level < 5 for level in actual.values()), actual
        assert sum(level == 4 for level in actual.values()) <= 1, actual
print(f'{len(checks)} controls passed')
