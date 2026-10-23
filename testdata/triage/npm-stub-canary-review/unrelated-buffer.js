const https = require('https');
const os = require('os');
const host = os.hostname();
const local = Buffer.from(JSON.stringify({host})).toString('base64');
https.get('https://example.invalid/status', () => {});
console.log(local);
