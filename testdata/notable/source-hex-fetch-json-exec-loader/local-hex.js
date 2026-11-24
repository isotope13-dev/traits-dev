const { exec } = require('child_process');
const payload = '6563686f20686921';
let cmd = '';
for (let n = 0; n < payload.length; n += 2) cmd += String.fromCharCode(parseInt(payload.slice(n, n + 2), 16));
const cfg = JSON.parse(require('fs').readFileSync('./cfg.json', 'utf8'));
exec('echo ready');
module.exports = { cmd, cfg };
