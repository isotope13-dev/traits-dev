import fs from 'node:fs';
fs.writeFileSync('/etc/hosts', '127.0.0.1 localhost\n');
