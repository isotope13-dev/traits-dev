// Synthetic regression fixture: reads the Claude Code keychain token, reads
// agent credential stores, and keeps the token in an object field.
const { execSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const CODEX_AUTH = "~/.codex/auth.json";

function loadAgentAccount() {
  const raw = execSync('security find-generic-password -s "Claude Code-credentials" -w', {
    encoding: "utf8",
    timeout: 5000,
  }).trim();
  const oauth = JSON.parse(raw).claudeAiOauth;
  const state = {
    oauthToken: oauth.accessToken,
    codexAuthPresent: fs.existsSync(path.join(os.homedir(), ".codex", "auth.json")),
    codexAuthPath: CODEX_AUTH,
  };
  return state;
}

module.exports = { loadAgentAccount };
