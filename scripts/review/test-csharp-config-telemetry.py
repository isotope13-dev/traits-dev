#!/usr/bin/env python3
"""Match the same processor and explicit telemetry setting in a method."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/os/package-manager/management::csharp-applyset-telemetry-disabled'
SOURCE = '''class Config {
  void Apply() {
    processor.GenerateTelemetryEvents = false;
    var result = processor.ApplySet(config, flags);
  }
}'''
cases = [
    ('same', SOURCE, True),
    ('other_processor', SOURCE.replace('processor.ApplySet', 'other.ApplySet'), False),
    ('enabled', SOURCE.replace('= false', '= true'), False),
    ('other_method', SOURCE.replace('ApplySet(', 'OpenConfigurationSet('), False),
    ('different_methods', SOURCE.replace('    var result', '  }\n  void Other() {\n    var result'), False),
]
with tempfile.TemporaryDirectory() as tmp:
    for name, source, expected in cases:
        path = Path(tmp) / (name + '.cs')
        path.write_text(source)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        found = any(t['id'] == RULE for f in json.loads(result.stdout)['files'] for t in f.get('traits', []))
        assert found == expected, (name, found)
print('C# configuration telemetry boundaries passed')
