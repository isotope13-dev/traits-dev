const https = require('https');
const options = {
  hostname: 'registry.example.net',
  port: 443,
  path: '/health',
  method: 'GET',
};
https.request(options).end();
