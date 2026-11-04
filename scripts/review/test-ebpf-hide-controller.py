#!/usr/bin/env python3
"""Keep process and file hide controller evidence distinct."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
source = '''void f() {
    hider_bpf__attach(skel);
    bpf_program__fd(skel->progs.hide_pid_make_it_disappear);
    bpf_map__fd(skel->maps.files_to_hide);
    bpf_map_update_elem(map, key, value, 0);
    add_blacklist_file(my_pid_str);
    add_blacklist_file(hide);
}
'''
cases = {'both.c': source,
         'no-program.c': source.replace('hide_pid_make_it_disappear', 'audit_pid'),
         'no-map-update.c': source.replace('bpf_map_update_elem', 'bpf_map_lookup_elem'),
         'no-self.c': source.replace('add_blacklist_file(my_pid_str)', 'observe_pid(my_pid_str)'),
         'no-file.c': source.replace('maps.files_to_hide', 'maps.audit_files')}
with tempfile.TemporaryDirectory(prefix='ebpf-hide-') as temp:
    root = Path(temp)
    for name, body in cases.items():
        (root / name).write_text(body)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / n) for n in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    process = 'objectives/evasion/process/concealment::ebpf-self-hide-pid-controller'
    file = 'objectives/evasion/file-hiding/query-filter::ebpf-file-hide-controller'
    assert process in found['both.c'] and file in found['both.c']
    for name in ('no-program.c', 'no-map-update.c'):
        assert process not in found[name] and file not in found[name]
    assert process not in found['no-self.c'] and file in found['no-self.c']
    assert file not in found['no-file.c'] and process in found['no-file.c']
    print('eBPF process and file hiding findings require their respective evidence.')
