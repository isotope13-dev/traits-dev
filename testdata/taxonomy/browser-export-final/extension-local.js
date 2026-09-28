const fs = require('fs');
const root = '/profile/Local Extension Settings';
const files = fs.readdirSync(root);
const info = fs.statSync(root);
files.push(root);
const bytes = fs.readFileSync(root + '/data');
console.log(bytes.length);
