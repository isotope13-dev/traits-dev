const https = require('https');

const body = JSON.stringify({ content: 'The service is online.' });
const request = https.request({
  hostname: 'discord.com',
  port: 443,
  path: '/api/webhooks/123/token',
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
});
request.end(body);
