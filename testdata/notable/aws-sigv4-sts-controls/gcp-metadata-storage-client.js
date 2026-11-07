const http = require('node:http');

function fetchDefaultServiceAccountToken() {
  return new Promise((resolve, reject) => {
    const req = http.get(
      {
        host: 'metadata.google.internal',
        path: '/computeMetadata/v1/instance/service-accounts/default/token',
        headers: { 'Metadata-Flavor': 'Google' },
      },
      (res) => {
        let data = '';
        res.on('data', (c) => (data += c));
        res.on('end', () => resolve(JSON.parse(data)));
      }
    );
    req.on('error', reject);
  });
}

async function listProjectBuckets(projectId) {
  const tok = await fetchDefaultServiceAccountToken();
  const res = await fetch(`https://storage.googleapis.com/storage/v1/b?project=${encodeURIComponent(projectId)}`, {
    headers: { Authorization: `Bearer ${tok.access_token}` },
  });
  return res.json();
}

module.exports = { listProjectBuckets };
