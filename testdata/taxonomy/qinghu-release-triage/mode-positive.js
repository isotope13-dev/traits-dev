const fs = require('node:fs');
fs.writeFileSync('config.json', JSON.stringify({token: 'configured'}), {
  encoding: 'utf-8',
  mode: 0o600,
});
const { mkdirSync } = require('node:fs');
mkdirSync('cache', { mode: 0o700 });
