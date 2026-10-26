const https = require('https');
https.get('https://198.51.100.19/status', {}, res => res.resume());
const unrelated = { rejectUnauthorized: false };
