const https = require('https');

const PKG_VERSION = '1.2.3';

// Ordinary update check: response is consumed, failures are reported, and
// nothing runs at import time.
function checkForUpdate(done) {
  https.get('https://registry.example.com/widget/latest', (res) => {
    let body = '';
    res.on('data', (chunk) => { body += chunk; });
    res.on('end', () => done(null, body));
  }).on('error', (err) => done(err));
}
module.exports = { checkForUpdate };
