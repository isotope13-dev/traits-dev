# /// script
# dependencies = ["pyyaml"]
# ///
"""Check that the relocated scheduled paths preserve the former system guard."""
import json
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[2]
audit = json.loads((root / 'taxonomy-migration/reviews/cap-99/scheduled-paths/moves.json').read_text())
expected = {x['new'] for x in audit['moves'] if x['old'].startswith('micro-behaviors/fs/path/config/system::')}
assert len(expected) == 9
p = root / 'objectives/lateral-movement/brute-force/iot-creds/uclibc-profile.yaml'
doc = yaml.safe_load(p.read_text())
helper = next(x for x in doc['composite_rules'] if x['id'] == 'system-or-scheduled-config-reference')
consumer = next(x for x in doc['composite_rules'] if x['id'] == 'uclibc-iot-credential-attack-shell-profile')
assert set(x['id'] for x in helper['any']) == expected | {'micro-behaviors/fs/path/config/system'}
assert {'id': 'system-or-scheduled-config-reference'} in consumer['all']
assert doc['defaults']['for'] == ['elf'] and helper['crit'] == 'component'
print('Scheduled path guard preserves the nine former system alternatives')
