#!/usr/bin/env python3
"""Discord admin and token-reply observations require matching bindings."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
ADMIN = 'micro-behaviors/data/collection/array::hardcoded-admin-id-insert-if-absent'
SELECT = 'micro-behaviors/communications/messaging/receive::admin-gated-target-refresh-selection'
REPLY = 'micro-behaviors/communications/messaging/send::target-token-refresh-attachment-reply'
HOSTILE = 'objectives/command-and-control/backdoor/control/discord::discord-hardcoded-admin-token-control'
SOURCE = '''
class Bot {
  constructor() {
    if (!this.adminIds.includes('123456789012345678')) {
      this.adminIds.push('123456789012345678');
    }
  }
  async select(interaction) {
    if (interaction.customId === 'select') {
      if (!this.adminIds.includes(interaction.user.id)) { return interaction.reply('no'); }
      const targetId = interaction.values[0];
      await this.handleManualRefresh(interaction, targetId, true);
    }
  }
  async handleManualRefresh(interaction, targetId, admin = false) {
    const filePath = path.join(this.dataDir, `${targetId}_token.json`);
    const oldData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const result = await this.callBackendAPI(oldData.refresh_token);
    if (result && result.success) {
      const safeData = { token: result.token, refresh_token: result.refresh_token };
      const buffer = Buffer.from(JSON.stringify(safeData));
      const attachment = new AttachmentBuilder(buffer);
      await interaction.editReply({ files: [attachment] });
    }
  }
}
'''
CASES = {
    'complete': (SOURCE, (True, True, True)),
    'different-id': (SOURCE.replace("push('123456789012345678')", "push('123456789012345679')"), (False, True, True)),
    'different-list': (SOURCE.replace('this.adminIds.push', 'this.otherIds.push'), (False, True, True)),
    'different-selected-user': (SOURCE.replace('interaction, targetId, true', 'interaction, other, true'), (True, False, True)),
    'different-input-file': (SOURCE.replace('readFileSync(filePath', 'readFileSync(other'), (True, True, False)),
    'different-result': (SOURCE.replace('refresh_token: result.refresh_token', 'refresh_token: other.refresh_token'), (True, True, False)),
    'different-reply': (SOURCE.replace('await interaction.editReply', 'await other.editReply'), (True, True, False)),
    'comment': ('/* ' + SOURCE + ' */', (False, False, False)),
}
with tempfile.TemporaryDirectory(prefix='discord-token-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.js')
        path.write_text(source)
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        ids = {trait['id'] for trait in report.get('traits', [])}
        found = tuple(rule in ids for rule in (ADMIN, SELECT, REPLY))
        assert found == CASES[name][1], (name, found, CASES[name][1])
        assert HOSTILE not in ids, (name, 'missing Discord invite webhook')
print('Discord admin selection and token reply require matching identities')
