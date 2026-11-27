'use strict';
const { execFileSync } = require('child_process');

// Print the last boot's warnings for a support bundle. No token is read.
function bootWarnings() {
  return execFileSync('journalctl', ['-b', '-p', 'warning', '--no-pager', '-o', 'short'], { encoding: 'utf8', timeout: 4000 });
}

module.exports = { bootWarnings };
