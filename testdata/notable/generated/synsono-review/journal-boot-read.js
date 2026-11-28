const cp = require('node:child_process');
const log = cp.execFileSync('journalctl', ['--no-pager', '-b']);
