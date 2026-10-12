const fs = require('fs');
const entries = fs.readdirSync('backups');
fs.unlinkSync(entries[0]);
