// Near miss (regression fixture, synthetic): a status API request and an
// unrelated local shell helper share a file but not a script download path.
const { spawn } = require("child_process");
const os = require("os");

async function readBalance(url, token) {
  const res = await fetch(url, { headers: { Authorization: "Bearer " + token } });
  if (!res.ok) throw new Error("HTTP " + res.status);
  return res.json();
}

function formatBalance(body) {
  const amount = Number(body && body.total_balance);
  if (!Number.isFinite(amount)) return "unknown";
  return amount.toFixed(2);
}

function describeHost() {
  return {
    platform: process.platform,
    arch: process.arch,
    release: os.release(),
    cpus: os.cpus().length,
    memory: os.totalmem(),
  };
}

function summarize(host, balance) {
  const lines = [];
  lines.push("platform " + host.platform + " " + host.arch);
  lines.push("release " + host.release);
  lines.push("cpus " + host.cpus);
  lines.push("memory " + host.memory);
  lines.push("balance " + formatBalance(balance));
  return lines.join("\n");
}

function restartLocalService(command) {
  // Restarts a service the user configured in their own shell profile.
  spawn("sh", ["-c", command], { stdio: "ignore" }).unref();
}

module.exports = { readBalance, describeHost, summarize, restartLocalService };
