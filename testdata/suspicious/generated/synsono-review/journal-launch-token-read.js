const cp = require('node:child_process');
const log = cp.execFileSync('journalctl', ['-b', '--no-pager']);
const token = log.match(/\?token=([A-Za-z0-9_-]+)/);
