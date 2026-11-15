const https = require('https');
const os = require('os');
const crypto = require('crypto');

const body = JSON.stringify({
  execution_id: crypto.randomUUID(),
  user: os.userInfo().username,
  platform: process.platform,
  arch: process.arch,
  cwd: process.cwd(),
  node: process.version,
});

const request = https.request('https://collector.example.net/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
});
request.write(body);
request.end();
