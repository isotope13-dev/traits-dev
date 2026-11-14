const http = require('http');
const body = JSON.stringify({ event: 'startup', version: '1.2.3' });
const req = http.request({
  hostname: 'telemetry.example.com',
  port: 443,
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
});
req.write(body);
req.end();
