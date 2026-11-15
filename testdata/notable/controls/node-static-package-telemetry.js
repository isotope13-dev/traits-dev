const http = require('http');

const payload = Buffer.from(JSON.stringify({ package: 'builder', version: '1.0.0' }));
const req = http.request({
  host: '127.0.0.1',
  port: 8000,
  method: 'POST',
  path: '/build-status',
}, () => {});
req.write(payload);
req.end();
