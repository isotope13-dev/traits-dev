const https = require('https');
const options = { hostname: 'example.invalid' };
options.rejectUnauthorized = false;
https.request(options).end();
