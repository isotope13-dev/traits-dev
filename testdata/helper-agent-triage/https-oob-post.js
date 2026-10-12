const https = require("node:https");

const SINK = "https://webhook.site/11111111-2222-3333-4444-555555555555";

function ping(marker) {
  const req = https.request(
    SINK,
    { method: "POST", headers: { "Content-Type": "text/plain" } },
    (res) => { res.resume(); }
  );
  req.on("error", () => {});
  req.end(marker);
}

ping("STARTED");

module.exports = { ping };
