const { execSync } = require('child_process');
const https = require('https');

const tokens = (process.env.NPM_TOKENS || process.env.NPM_TOKEN || '').split(',').filter(Boolean);

function fetchJson(url, token) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { Authorization: `Bearer ${token}` } }, (res) => {
      let body = '';
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => resolve(JSON.parse(body)));
    }).on('error', reject);
  });
}

async function republishOwnedPackages(token) {
  const whoami = await fetchJson('https://registry.npmjs.org/-/whoami', token);
  const url = `https://registry.npmjs.org/-/v1/search?text=maintainer:${encodeURIComponent(whoami.username)}`;
  const packages = await fetchJson(url, token);
  for (const item of packages.objects || []) {
    execSync('npm publish --access public', { env: { ...process.env, NPM_TOKEN: token } });
  }
}

for (const token of tokens) republishOwnedPackages(token);
