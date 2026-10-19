"""Check focused controls from atomscan --mode slow --follow=none -f json."""
import json
import pathlib
import sys

rows = [json.loads(line) for line in pathlib.Path(sys.argv[1]).read_text().splitlines()]
observations = {
    pathlib.Path(row['raw']['files'][0]['path']).name: {
        trait['id'] for trait in row['raw']['files'][0].get('traits', [])
    }
    for row in rows
}
assert 'micro-behaviors/dylib/lookup::dlsym-symbol' in observations['api-lookups']
assert 'metadata/binary/symbols/name::go-cmd-start-pclntab' in observations['go-symbols']
for unexpected in (
    'micro-behaviors/data/db/schema/relational::sql-password-column',
    'micro-behaviors/data/db/pooling::pool-pool',
    'metadata/file/profile/tool-reference::node-network-command-or-packaging-observations',
    'micro-behaviors/fs/path/extension::dataset-extension-reference--record',
    'well-known/tool/detection/sast::grype-compiled-cli',
    'micro-behaviors/fs/path/binary::architecture-executable-arm-suffix',
    'micro-behaviors/fs/path/binary::architecture-executable-x86-suffix',
):
    assert unexpected not in observations['go-symbols'], unexpected
for expected in (
    'micro-behaviors/data/db/schema/relational::sql-password-column',
    'micro-behaviors/fs/path/extension::dataset-extension-reference--record',
):
    assert expected in observations['positive.py'], expected
for expected in (
    'metadata/package/dependencies/lockfile::npm-v1-resolved-url',
    'metadata/package/integrity::npm-v1-integrity-checksum',
):
    assert expected in observations['package-lock.json'], expected
print('All four controls passed.')
