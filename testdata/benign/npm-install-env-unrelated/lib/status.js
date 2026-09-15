const https = require("https");

// An independent API sends only a fixed build-status document.
exports.reportBuild = function reportBuild() {
  const body = JSON.stringify({ status: "ready" });
  const req = https.request({
    hostname: "build-status.example.invalid",
    path: "/status",
    method: "POST",
    headers: { "Content-Type": "application/json" }
  }, () => {});
  req.on("error", () => {});
  req.end(body);
};
