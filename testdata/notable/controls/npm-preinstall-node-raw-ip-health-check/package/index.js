const http = require("http");

const request = http.request({
  hostname: "75.119.159.178",
  port: 7891,
  path: "/health",
  method: "POST"
});
request.write(JSON.stringify({ status: "ok" }));
request.end();
