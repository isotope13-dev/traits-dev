// Benign SSH authorized_keys audit helper: reads authorized_keys via a bound
// path.join variable and writes JSON audit output to a different path variable.
// Commented-out appendFileSync must also remain inert.
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

function auditAuthorizedKeys(outDir) {
  const home = os.homedir();
  const sshDir = path.join(home, ".ssh");
  const ak = path.join(sshDir, "authorized_keys");
  const reportFile = path.join(outDir, "ssh-key-inventory.json");

  // Never mutate user keys in audit mode: fs.appendFileSync(ak, "ssh-ed25519 ...\n");
  let raw = "";
  if (fs.existsSync(ak)) {
    raw = fs.readFileSync(ak, "utf8");
  }
  const keyCount = raw
    .split(/\r?\n/)
    .filter((line) => line.trim() && !line.trim().startsWith("#")).length;

  fs.writeFileSync(reportFile, JSON.stringify({ keyCount }, null, 2));
  return keyCount;
}

module.exports = { auditAuthorizedKeys };
