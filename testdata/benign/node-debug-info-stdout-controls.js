// Benign control for full-fingerprint (appium 4.0.0-beta triage): a
// diagnostic command assembling the host profile and printing it to
// local stdout for the invoking user. Printed, not exfiltrated, so the
// comprehensive-fingerprinting composite must stay silent.
const os = require("node:os");
function showDebugInfo() {
  const debugInfo = {
    os: `${os.platform()} ${os.arch()} ${os.release()}`,
    node: process.version,
    user: os.userInfo().username,
    home: os.homedir(),
  };
  console.log(JSON.stringify(debugInfo, null, 2));
}
module.exports = { showDebugInfo };
