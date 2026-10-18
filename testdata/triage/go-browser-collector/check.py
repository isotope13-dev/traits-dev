"""Static parser/provenance controls; never compile or execute the Go fixtures."""
import argparse
import json
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--work-dir', type=Path, required=True)
ap.add_argument('--cleave', default='cleave')
ap.add_argument('--traits-dir', type=Path, default=Path('.'))
a = ap.parse_args()
a.work_dir.mkdir(parents=True, exist_ok=True)
sweep = 'objectives/credential-access/browser/multi-target::go-login-store-sweep'
autorun = 'objectives/persistence/login/registry/run-key::go-self-image-read-run-key-writes'
selfread = 'micro-behaviors/fs/read/self::go-read-own-executable'
name = 'metadata/file/function::backdoor-exploit-function-name'
# Arbitrary names, two distinct browser stores, and the same bytes read and kept.
source = r'''package main
import ("os"; "path/filepath"; "golang.org/x/sys/windows/registry")
func gather() [][]byte {
 root := os.Getenv("LOCALAPPDATA")
 paths := []string{
  filepath.Join(root, `Microsoft\Edge\User Data\Default\Login Data`),
  filepath.Join(root, `Google\Chrome\User Data\Default\Login Data`),
 }
 var collected [][]byte
 for _, file := range paths {
  if content, err := os.ReadFile(file); err == nil {
   collected = append(collected, content)
  }
 }
 return collected
}
func main() {
 image, _ := os.Executable()
 contents, _ := os.ReadFile(image)
 _ = os.WriteFile("helper.exe", contents, 0755)
 key, _, _ := registry.CreateKey(registry.CURRENT_USER,
  `Software\Microsoft\Windows\CurrentVersion\Run`, registry.SET_VALUE)
 _ = key.SetStringValue("Helper", "helper.exe")
 _ = gather()
}
'''
cases = [
 ('renamed', source, {sweep: True, autorun: True, selfread: True, name: False}),
 ('unrelated-read', source.replace('os.ReadFile(file)', 'os.ReadFile("settings.json")'),
  {sweep: False, autorun: True, selfread: True}),
 ('unrelated-image-read', source.replace('os.ReadFile(image)', 'os.ReadFile("settings.json")'),
  {sweep: True, autorun: False, selfread: False}),
 ('no-accumulation', source.replace('append(collected, content)', 'append(collected, []byte("status"))'),
  {sweep: False, autorun: True}),
 ('duplicate-store', source.replace(r'Google\Chrome', r'Microsoft\Edge'),
  {sweep: False, autorun: True}),
 ('no-run-key', source.replace(r'CurrentVersion\Run', r'CurrentVersion\Settings'),
  {sweep: True, autorun: False}),
 ('comment-only', '// backdoor (svchost32)\npackage main\nfunc main() {}\n',
  {sweep: False, autorun: False, name: False}),
 ('real-function', 'package main\nfunc backdoor() {}\nfunc main() {}\n',
  {name: True, sweep: False, autorun: False}),
 ('display-name-only', 'package main\nconst text = "Cloud Sync Service"\nconst file = "svchost32.exe"\n',
  {sweep: False, autorun: False,
   'well-known/malware/rat/cornflake::cornflake-cloud-sync-service-name': False,
   'well-known/malware/rat/cornflake::cornflake-svchost32-basename': False,
   'micro-behaviors/os/service/configure::cloud-sync-display-name-reference': True}),
]
files=[]
for label, content, _ in cases:
 path = a.work_dir / (label + '.go')
 path.write_text(content)
 files.append(path)
# One parser run for the whole set, with no network/dependency following.
r = subprocess.run([a.cleave, '--traits-dir', str(a.traits_dir.resolve()),
                    '--format', 'json', *map(str, files)],
                   text=True, capture_output=True, check=True)
(a.work_dir / 'controls.json').write_text(r.stdout)
reports=[]
decoder=json.JSONDecoder()
remaining=r.stdout.strip()
while remaining:
 report, end=decoder.raw_decode(remaining)
 reports.extend(report.get('files', [report]))
 remaining=remaining[end:].lstrip()
results=[]
for label, _, expected in cases:
 matches=[f for f in reports if Path(f['path']).name == label + '.go']
 assert len(matches) == 1, (label, [f['path'] for f in reports])
 actual={t['id'] for t in matches[0].get('traits',[])}
 # Some renderers spell findings instead of traits.
 actual.update(t['id'] for t in matches[0].get('findings',[]))
 for trait, wanted in expected.items():
  assert (trait in actual) == wanted, (label, trait, wanted, sorted(actual))
 results.append({'case': label, 'checks': len(expected), 'passed': True})
print(json.dumps(results, indent=2))
