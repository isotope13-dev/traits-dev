const https = require('https');
const os = require('os');

function showLocalHostname() {
  console.log(encodeURIComponent(String(os.hostname()).replace(/[^a-zA-Z0-9.-]/g, '_').slice(0, 63)));
}

function checkService() {
  return https.get('https://telemetry.example.test/health', res => res.resume());
}

module.exports = { showLocalHostname, checkService };
