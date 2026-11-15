const https = require('https');
const args = process.argv.slice(2);
const data = encodeURIComponent(args.join(' '));
https.get(`https://api.example.com/submit/${data}`);
