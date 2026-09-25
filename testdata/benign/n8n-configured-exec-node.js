// Configured-exec n8n community node (benign control).
//
// Executes an administrator-configured binary path. The command never comes
// from the workflow payload, there is no shared-secret gate, and nothing is
// downloaded or staged executable — so the trojanized-node composites must
// not fire even though child_process exec and n8n environment references
// are present.
const { exec } = require('child_process');

class ConfigExec {
  constructor() {
    this.description = {
      displayName: 'Config Exec',
      name: 'configExec',
      group: ['transform'],
      version: 1,
      description: 'Runs the configured helper binary',
      defaults: { name: 'Config Exec' },
      inputs: ['main'],
      outputs: ['main'],
      properties: [
        {
          displayName: 'Helper Path',
          name: 'helperPath',
          type: 'string',
          default: '',
        },
      ],
    };
  }

  async execute(items) {
    const helperPath = this.getNodeParameter('helperPath', 0);
    if (process.env.N8N_RUNNERS_ENABLED !== 'true') {
      return items;
    }
    const result = await new Promise((resolve) => {
      exec(String(helperPath), (e, so, se) => {
        resolve({ ok: !e, out: `${so || ''}${se || ''}` });
      });
    });
    items[0].json = Object.assign({}, items[0].json, { r: result });
    return items;
  }
}

module.exports = { ConfigExec };
