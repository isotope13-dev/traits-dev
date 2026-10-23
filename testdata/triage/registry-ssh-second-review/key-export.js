const fs = require('fs');
const authorizedKeysExport = '/tmp/release.pub';
fs.appendFileSync(authorizedKeysExport, "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO7H3kK/1BfG72Dh4JPI/663twZhFrhkcM/I2Bmrm09a review@invalid.test");
