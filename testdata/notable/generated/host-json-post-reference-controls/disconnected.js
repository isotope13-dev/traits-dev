const http = require('http');
const os = require('os');
console.log(os.hostname(), process.cwd());
const body = JSON.stringify({ ready: true });
const request = http.request('http://203.0.113.16/status', { method: 'POST' });
request.write(body);
request.end();
