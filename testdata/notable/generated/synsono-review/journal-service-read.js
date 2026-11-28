const cp = require('node:child_process');
const log = cp.spawnSync('journalctl', ['-u', unit, '--since', since, '--no-pager']);
