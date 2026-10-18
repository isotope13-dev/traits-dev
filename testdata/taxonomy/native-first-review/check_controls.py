"""Check the generated controls' complete emitted reports, not just matches."""
import json
import sys
from pathlib import Path

http = 'micro-behaviors/communications/http/client/wininet::compact-urlmon-extended-api-set'
cn = 'micro-behaviors/data/config/syntax::cryptonight-pool-json'
wallet = 'micro-behaviors/data/config/syntax::wallet-json-donations-disabled'
builtin = 'well-known/app/finance/xmrig::built-in-wallet-pools-config'
stratum = 'well-known/app/finance/xmrig::stratum-pools-donations-disabled'
expected = {
    'http-apis.exe': {http},
    'http-missing-extended.exe': set(),
    'mining-config.exe': {cn, wallet, builtin, stratum},
    'mining-config-no-cn.exe': {wallet, builtin, stratum},
    'mining-config-donate.exe': {cn, builtin},
}
selected = {http, cn, wallet, builtin, stratum}
seen = set()
for line in Path(sys.argv[1]).read_text().splitlines():
    for file in json.loads(line)['files']:
        name = Path(file['path']).name
        assert name in expected, name
        traits = file['traits']
        assert not [t for t in traits if t['crit'] >= 4], name
        got = {t['id'] for t in traits} & selected
        assert got == expected[name], (name, got, expected[name])
        assert all(t['crit'] == 3 for t in traits if t['id'] in selected), name
        seen.add(name)
assert seen == set(expected), seen
print('PASS: 5 inert PE controls; accurate notable coverage; no suspicious/hostile findings')
