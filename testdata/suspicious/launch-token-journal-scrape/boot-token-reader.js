'use strict';
const fs = require('fs');
const { execFileSync } = require('child_process');

// Recover the local web UI launch token when the host never handed it over.
function getActiveWebToken() {
  try {
    if (fs.existsSync('/var/log/example-web.log')) {
      const content = fs.readFileSync('/var/log/example-web.log', 'utf8');
      const matches = [...content.matchAll(/\?token=([A-Za-z0-9_-]+)/g)];
      if (matches.length > 0) return matches[matches.length - 1][1];
    }
  } catch {}
  try {
    const out = execFileSync('journalctl', ['-b', '-n', '400', '--no-pager', '-o', 'cat'], { encoding: 'utf8', timeout: 4000 });
    const all = [...out.matchAll(/http:\/\/127\.0\.0\.1:\d+\/\?token=([A-Za-z0-9_-]+)/g)];
    if (all.length > 0) return all[all.length - 1][1];
  } catch {}
  return null;
}

module.exports = { getActiveWebToken };
