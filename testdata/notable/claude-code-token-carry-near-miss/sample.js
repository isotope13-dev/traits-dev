// Synthetic regression near miss: a usage check reads the keychain token for one
// request and never stores it in an object field or reads other agent stores.
const { execSync } = require("child_process");

function claudeUsageRequest() {
  const raw = execSync('security find-generic-password -s "Claude Code-credentials" -w', {
    encoding: "utf8",
  }).trim();
  const token = JSON.parse(raw).claudeAiOauth.accessToken;
  return fetch("https://api.anthropic.com/api/oauth/usage", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

module.exports = { claudeUsageRequest };
