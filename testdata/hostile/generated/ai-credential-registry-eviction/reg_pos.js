const { spawnSync } = require('child_process');
// Remove the persisted provider key from the user environment
spawnSync('reg.exe', ['delete', 'HKCU\\Environment', '/v', 'ANTHROPIC_API_KEY', '/f']);
