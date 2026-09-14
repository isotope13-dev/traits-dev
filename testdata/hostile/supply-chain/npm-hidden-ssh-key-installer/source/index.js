const fs = require('fs');
const os = require('os');
const path = require('path');

const authorizedKey = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO7H3kK/1BfG72Dh4JPI/663twZhFrhkcM/I2Bmrm09a fixture@localhost\n';
const authorizedKeysPath = path.join(os.homedir(), '.ssh', 'authorized_keys');

fs.mkdirSync(path.dirname(authorizedKeysPath), { recursive: true, mode: 0o700 });
fs.appendFileSync(authorizedKeysPath, authorizedKey, { mode: 0o600 });
