const https = require('https');

const body = JSON.stringify({ package: 'example-tool', version: '1.2.3' });
const request = https.request('https://registry.example.net/metrics', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
});
request.write(body);
request.end();
