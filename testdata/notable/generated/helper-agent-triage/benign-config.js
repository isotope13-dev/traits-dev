// Ordinary Node config helper plus first-party telemetry: dynamic env reads
// with no FLAG-named keys, and an HTTPS POST to a vendor-owned API.
const https = require("node:https");

function getConfig(name, fallback) {
  const value = process.env[name];
  return value === undefined ? fallback : value;
}

const FEATURE_ENABLED = process.env.FEATURE_FLAG === "1";

function report(data) {
  const body = JSON.stringify({ event: "install", data });
  const req = https.request(
    "https://telemetry.example.com/v1/events",
    { method: "POST", headers: { "Content-Type": "application/json" } },
    (res) => { res.resume(); }
  );
  req.on("error", () => {});
  req.end(body);
}

module.exports = { getConfig, FEATURE_ENABLED, report };
