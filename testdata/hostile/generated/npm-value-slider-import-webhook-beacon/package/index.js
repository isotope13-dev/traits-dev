const https = require('https');

const url = 'https://webhook.site/11111111-2222-4333-8444-555555555555';
const options = { method: 'POST' };
const request = https.request(url, options);
request.end(JSON.stringify({ package: 'depconf-marker' }));
