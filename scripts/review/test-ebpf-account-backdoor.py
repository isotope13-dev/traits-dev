#!/usr/bin/env python3
"""Require the targeted branches and BPF interception for backdoor findings."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
common = '''SEC("tp/syscalls/sys_exit_read")
int f(void) { bpf_map_lookup_elem(&backdoor_trigger, &key);
  bpf_probe_write_user(dst, src, size);
'''
key = 'if (file_type == AUTHORIZED_KEYS && args->backdoor_type == AUTH_BACKDOOR) action();\n'
account = 'if (file_type == PASSWD || file_type == SHADOW) action();\n'
controller = '''char *path = "/etc/shadow";
char *key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHgLzgvt+dvcDklpa1+j0fiaodAaHIP552JCnmDw00to";
void f() { hidden_ssh_bpf__open(); bpf_map_update_elem(map, a, b, 0);
memcpy(buffer, backdoor_hashed_passwd, len);
set_backdoor_pubkey(backdoor_publickey, len); set_port(2345, AUTH_BACKDOOR); }
'''
cases = {'key.c': common + key + '}', 'account.c': common + account + '}',
         'no-write.c': common.replace('bpf_probe_write_user(dst, src, size);', '') + key + account + '}',
         'generic.c': common + 'action(); }', 'controller.c': controller,
         'no-bpf.c': controller.replace('bpf_map_update_elem', 'ordinary_update'),
         'no-auth-port.c': controller.replace('AUTH_BACKDOOR', 'NORMAL_MODE'),
         'no-password-copy.c': controller.replace('backdoor_hashed_passwd', 'ordinary_hash')}
with tempfile.TemporaryDirectory(prefix='ebpf-backdoor-') as temp:
    root = Path(temp)
    for name, source in cases.items():
        (root / name).write_text(source)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / name) for name in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    key_id = 'objectives/lateral-movement/ssh/backdoor::ebpf-authorized-key-read-backdoor'
    account_id = 'objectives/command-and-control/backdoor/account::ebpf-account-read-backdoor'
    assert key_id in found['key.c'] and account_id not in found['key.c']
    assert account_id in found['account.c'] and key_id not in found['account.c']
    for name in ('no-write.c', 'generic.c'):
        assert key_id not in found[name] and account_id not in found[name], (name, found[name])
    controller_key = 'objectives/lateral-movement/ssh/backdoor::ebpf-ssh-backdoor-controller'
    controller_account = 'objectives/command-and-control/backdoor/account::ebpf-account-backdoor-controller'
    assert controller_key in found['controller.c'] and controller_account in found['controller.c']
    assert controller_key not in found['no-bpf.c'] and controller_account not in found['no-bpf.c']
    assert controller_key not in found['no-auth-port.c']
    assert controller_account not in found['no-password-copy.c']
    print('eBPF account and key backdoor findings require their distinct evidence.')
