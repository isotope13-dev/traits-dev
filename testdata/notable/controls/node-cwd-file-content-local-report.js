const fs = require('fs');
const path = require('path');
const files = fs.readdirSync(process.cwd());
const summary = files.map(file => ({ name: file, bytes: fs.statSync(path.join(process.cwd(), file)).size }));
fs.writeFileSync(path.join(process.cwd(), 'file-summary.json'), JSON.stringify(summary));
