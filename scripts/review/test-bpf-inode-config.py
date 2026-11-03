#!/usr/bin/env python3
"""Check that inode collection needs BPF hide configuration."""
import json
import pathlib
import subprocess
import tempfile

sample = """
void configure() {
  auto setting = config["bpf_program_config"]["hide_payload"];
  auto inode = utils::get_inode_of_process(payload_pid);
  bpfConf.inodes.push_back(inode);
  for (auto file : config["bpf_program_config"]["files_to_hide"]) {
    auto inode = utils::get_inode_of_file(file);
    bpfConf.inodes.push_back(inode);
  }
}
"""
cases = {
    'hide-config': (sample, True),
    'no-payload-hide': (sample.replace('"hide_payload"', '"monitor_payload"'), False),
    'no-file-hide': (sample.replace('"files_to_hide"', '"files_to_monitor"'), False),
    'no-process-inode': (sample.replace('get_inode_of_process', 'get_process_info'), False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (content, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.cpp')
        path.write_text(content)
        data = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::bpf-hide-inode-configuration') for t in data['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('BPF inode concealment configuration boundaries passed.')
