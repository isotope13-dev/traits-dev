const fs = require('node:fs');
fs.writeFileSync('config.json', '{}');
const options = { mode: 0o600 };
