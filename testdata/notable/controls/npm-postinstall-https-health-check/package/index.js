const https = require("https");

const request = https.request({
  hostname: "status.example.net",
  method: "POST",
  headers: { "Content-Type": "application/json" }
});
request.write(JSON.stringify({ status: "ok" }));
request.end();
