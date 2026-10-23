const https = require('https');
const encoded = Buffer.from(JSON.stringify({sample: true})).toString('base64');
https.get(`https://example.invalid/log?data=${encoded}`, () => {});
