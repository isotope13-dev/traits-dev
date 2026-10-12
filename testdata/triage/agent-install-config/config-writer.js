const fs = require('fs');
const mcpServers = { helper: { command: 'npx', args: ['helper'] } };
fs.writeFileSync('settings.json', JSON.stringify({ mcpServers }));
