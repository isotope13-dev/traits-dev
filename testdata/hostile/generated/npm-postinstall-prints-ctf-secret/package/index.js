const fs = require('fs');

let flag = process.env.FLAG || '';
try {
  flag = flag || fs.readFileSync('/usr/src/app/flag', 'utf8').trim();
} catch (_) {}

console.log('CTF flag:', flag);
