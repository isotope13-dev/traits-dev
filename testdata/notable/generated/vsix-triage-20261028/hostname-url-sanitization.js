const https = require('https');
const os = require('os');

function reportHostname() {
  const host = encodeURIComponent(
    String(os.hostname() || 'unknown').replace(/[^a-zA-Z0-9.-]/g, '_').slice(0, 63)
  );
  return https.get('https://telemetry.example.test/host/' + host, res => res.resume());
}

module.exports = { reportHostname };
