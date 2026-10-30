# /// script
# dependencies = ["pyyaml"]
# ///
"""Check that app-data directory consumers retain moved browser paths."""
from pathlib import Path
import json
import yaml

root = Path(__file__).resolve().parents[2]
moves = json.loads((root / 'taxonomy-migration/reviews/cap-99/browser-paths/moves.json').read_text())['moves']
expected = {row['new'] for row in moves}
assert len(expected) == 6
consumers = {
    'metadata/file/profile/network/dns-resource-observations.yaml': 'dns-lookup-label-encoding-beside-resource-references',
    'metadata/file/profile/network/subject-review4-go-resource-observations.yaml': 'go-post-beside-file-read-and-path-references',
    'micro-behaviors/fs/read/file/target/node-resource-path.yaml': 'node-file-read-near-resource-path',
}
for name, rule_id in consumers.items():
    data = yaml.safe_load((root / name).read_text())
    rule = next(r for r in data['composite_rules'] if r['id'] == rule_id)
    alternatives = {item['id'] for item in rule['any']}
    assert 'micro-behaviors/fs/path/app-data/' in alternatives
    assert expected <= alternatives, (name, expected - alternatives)
print('Browser-path consumers retain all six moved alternatives.')
