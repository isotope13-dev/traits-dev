const http = require('http');
const os = require('os');
const body = JSON.stringify({ hostname: os.hostname(), cwd: process.cwd() });
const req = http.request('http://127.0.0.1:4555/status', { method: 'POST' });
req.write(body);
req.end();
