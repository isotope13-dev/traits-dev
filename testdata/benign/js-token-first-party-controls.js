// First-party token round-trip control: reads the cached SSO token and
// POSTs its refresh grant back to its own issuers (Kiro + AWS OIDC).
// The first-party unless legs must suppress the artifact-upload hostile.
const fs = require('fs');
const os = require('os');
const region = 'us-east-1';
const p = require('path').join(os.homedir(), '.aws', 'sso', 'cache', 'kiro-auth-token.json');
const t = JSON.parse(fs.readFileSync(p, 'utf8'));
fetch('https://prod.us-east-1.auth.desktop.kiro.dev/refreshToken', {
  method: 'POST',
  body: JSON.stringify({ refreshToken: t.refreshToken }),
});
fetch(`https://oidc.${region}.amazonaws.com/token`, {
  method: 'POST',
  body: JSON.stringify({ grantType: 'refresh_token', refreshToken: t.refreshToken }),
});
