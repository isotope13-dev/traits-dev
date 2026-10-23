const https = require('https');
const encoded = Buffer.from('diagnostic').toString('hex');
https.get(`https://example.invalid/log?data=${encoded}`, () => {});
