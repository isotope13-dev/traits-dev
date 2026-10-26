'use strict';
// Claude-branded helper that only reads local config. No gateway
// endpoint, no lookalike origin: brand strings alone convict nothing.
const fs = require('fs');
const path = require('path');
const os = require('os');

function showStatus() {
  console.log('Claude Desktop Setup status');
  const file = path.join(os.homedir(), '.claude', 'settings.json');
  const raw = fs.readFileSync(file, 'utf8');
  return JSON.parse(raw);
}

module.exports = { showStatus };
