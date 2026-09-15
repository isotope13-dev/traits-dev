// An administrator's opt-in, recurring service health check.
const { execSync } = require('node:child_process');
const cp = require('node:child_process');

function installHealthCheck() {
  execSync("(crontab -l 2>/dev/null; echo '*/23 * * * * curl -fsSL https://health.example.invalid/status >/dev/null 2>&1 # example-health') | crontab -");
}

// This independent diagnostic has no relationship to the scheduled command.
function runtimeVersion() {
  return cp.spawn('node', ['--version']);
}

module.exports = { installHealthCheck, runtimeVersion };
