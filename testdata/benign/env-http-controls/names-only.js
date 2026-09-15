const https = require('https');

function configuredCredentialNames() {
  return Object.keys(process.env).filter(name => /TOKEN|SECRET|PASSWORD/.test(name));
}

function reportStatus() {
  const body = JSON.stringify({ status: 'ready' });
  const request = https.request('https://status.example.org/health', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }
  });
  request.write(body);
  request.end();
}

module.exports = { configuredCredentialNames, reportStatus };
