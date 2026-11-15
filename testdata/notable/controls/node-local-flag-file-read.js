const fs = require('fs');
const flag = fs.readFileSync('/tmp/flag.txt', 'utf8');
console.log(flag);
