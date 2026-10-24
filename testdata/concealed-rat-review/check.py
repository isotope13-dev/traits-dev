"""Check saved cleave reports from the generated controls (see REVIEW.md)."""
import json, pathlib, sys

def reports(path):
    text = pathlib.Path(path).read_text(); decoder = json.JSONDecoder(); pos = 0
    result = {}
    while text[pos:].strip():
        while text[pos].isspace(): pos += 1
        report, pos = decoder.raw_decode(text, pos)
        for file in report['files']:
            result[pathlib.Path(file['path']).name] = {t['id'] for t in file['traits']}
    return result

actual = reports(sys.argv[1]); before = reports(sys.argv[2])
mapper = 'micro-behaviors/process/inject/runtime/call::go-x86-pe-map-entry-dispatch'
exclusion = 'objectives/evasion/anti-av/exclusion::xor-hidden-defender-path-process-exclusions'
persistence = 'objectives/persistence/login/registry/run-key::concealed-mapper-run-key-registration'
keylog = 'objectives/collection/keylog/polling::cil-key-state-window-record-pattern'
wipe = 'objectives/impact/wipe/disk/mbr::mbr-wiper-pe'
nc = 'micro-behaviors/communications/socket/netcat::nc-native-command-bytes'
port = 'micro-behaviors/data/db/mongodb::native-client-port-token'
stack = 'micro-behaviors/data/string/assembly::native-immediate-string'
expected = {
    'mapper-exclusions-run.exe': ({mapper,exclusion,persistence},set()),
    'mapper-only.exe': ({mapper},{exclusion,persistence}),
    'encoded-data-only.exe': ({'objectives/evasion/anti-av/exclusion::xor-hidden-defender-exclusion-command'},{mapper,persistence,exclusion}),
    'different-xor-keys.exe': ({mapper},{exclusion,persistence}),
    'key-recording.exe': ({keylog},set()),
    'key-polling-only.exe': (set(),{keylog}),
    'different-record-fields.exe': (set(),{keylog}),
    'sector-taunt.exe': ({wipe},set()),
    'sector-writer-only.exe': (set(),{wipe}),
    'taunt-only.exe': (set(),{wipe}),
    'command-and-port.exe': ({nc,port},set()),
    'identifier-and-padding.exe': (set(),{nc,port}),
    'native-path-immediates.exe': ({stack},set()),
    'headings.md': ({'metadata/file/profile/markup::at-least-four-markdown-section-headings'},set()),
    'controls.sh': ({'micro-behaviors/communications/socket/netcat::nc-other-command-text',
                     'micro-behaviors/data/db/mongodb::script-client-port-token'},set()),
    'hex-netcat-loop.sh': ({'micro-behaviors/communications/socket/netcat::nc-other-command-text',
                           'micro-behaviors/communications/socket/netcat::nc-pipe'},set()),
}
for name,(positive,negative) in expected.items():
    assert name in actual, name
    assert positive <= actual[name], (name,'missing',positive-actual[name])
    assert not negative & actual[name], (name,'unexpected',negative&actual[name])
# Retain pre-existing attack objectives on real source fixtures, independently
# of the renamed native/source primitives. Union composites still resolve for
# consumers; cleave intentionally omits simple any-unions from emitted output.
for name in ['controls.sh','hex-netcat-loop.sh']:
    objectives = {x for x in before[name] if x.startswith('objectives/')}
    assert objectives <= actual[name], (name,'lost objectives',objectives-actual[name])
assert stack in before['native-path-immediates.exe']
assert 'micro-behaviors/communications/socket/netcat::nc' in before['command-and-port.exe']
assert 'micro-behaviors/data/db/mongodb::client-port-reference' in before['command-and-port.exe']
print('16 positive/near-miss controls passed; existing source objectives retained')
