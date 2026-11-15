const http = require("http");

const request = http.request({
  hostname: "collector.oast-cn.byted-dast.com",
  path: "/health",
  method: "GET"
});
request.end();
