'use strict';
const { execFile } = require('child_process');

async function installToolchain(vendorUrl) {
  const res = await fetch(vendorUrl);
  const script = await res.text();
  const encoded = Buffer.from(script, 'utf16le').toString('base64');
  execFile('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-EncodedCommand', encoded]);
}

module.exports = { installToolchain };
