// Benign control for the printf-fed Base64 transport: every word of the
// emitted command is an interpolation or a fixed token, so exec layers that
// re-split quoting still deliver the launcher byte-for-byte. No static blob.
const { execFileSync } = require("node:child_process");
function base64(value) {
  return Buffer.from(value, "utf8").toString("base64");
}
function launcherCommand(launcherSource, payload) {
  return `printf %s ${base64(launcherSource)} | base64 -d | sh -s ${base64(launcherSource)} ${base64(payload)}`;
}
module.exports = { launcherCommand };
