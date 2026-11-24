// Maintains a local development hosts block for named test services.
const { execSync } = require("child_process");

const hostsPath = "/etc/hosts";
const names = ["web.dev.test", "api.dev.test"];
const body = names.map((h) => `127.0.0.1 ${h}`).join("\n");
execSync(`printf '%s' '${body}' | tee ${hostsPath} > /dev/null`);
