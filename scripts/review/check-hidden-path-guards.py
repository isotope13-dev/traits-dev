# /// script
# dependencies = ["pyyaml"]
# ///
"""Check former location/temp directory selectors after hidden-path moves."""
import json
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[2]
audit = json.loads((root / 'taxonomy-migration/reviews/cap-99/hidden-paths/moves.json').read_text())
loc = {x['new'] for x in audit['moves'] if x['old'].startswith('micro-behaviors/fs/path/location::')}
tmp = {x['new'] for x in audit['moves'] if x['old'].startswith('micro-behaviors/fs/path/temp::')}
assert (len(loc), len(tmp)) == (17, 10)
def rule(path, identifier):
    doc = yaml.safe_load((root / path).read_text())
    return next(x for x in doc['composite_rules'] if x['id'].split('::')[-1] == identifier)
for path, identifier, old, moved in [
    ('objectives/evasion/file-hiding/dotfile-create/hidden-path-review-guard.yaml', 'location-or-former-hidden-path', 'micro-behaviors/fs/path/location/', loc),
    ('objectives/command-and-control/dropper/delivery/http/hidden-path-review-guard.yaml', 'temp-or-former-hidden-path', 'micro-behaviors/fs/path/temp/', tmp),
]:
    assert {x['id'] for x in rule(path, identifier)['any']} == moved | {old}
for path, identifier, old, moved in [
    ('micro-behaviors/communications/http/download/webclient/downloadfile.yaml', 'webclient-downloadfile-exe', 'micro-behaviors/fs/path/location/', loc),
    ('objectives/anti-static/obfuscation/steganography/lsb/execution-context.yaml', 'embedded-image-lsb-drop-executor', 'micro-behaviors/fs/path/temp/', tmp),
]:
    alternatives = {x['id'] for x in rule(path, identifier)['any']}
    assert moved | {old} <= alternatives
for path, identifier, helper in [
    ('objectives/evasion/file-hiding/dotfile-create/generic.yaml', 'native-hidden-dotfile-staging', 'location-or-former-hidden-path'),
    ('objectives/command-and-control/dropper/delivery/http/python.yaml', 'python-dropper', 'temp-or-former-hidden-path'),
]:
    consumer = rule(path, identifier)
    assert {'id': helper} in consumer['all']
    assert 'near_bytes' not in consumer and 'near_lines' not in consumer
print('Hidden path directory selectors preserve all 27 moved alternatives')
